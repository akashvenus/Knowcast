"""Tests for the complete initial database schema metadata."""

from app import models
from app.db.base import Base
from sqlalchemy import UniqueConstraint
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.sql.sqltypes import Uuid


def test_all_engineering_brief_entities_are_registered() -> None:
    assert set(Base.metadata.tables) == {
        "users",
        "sources",
        "newsletters",
        "content_blocks",
        "image_assets",
        "audio_assets",
        "audio_segments",
        "ingestion_jobs",
        "playback_progress",
    }
    assert len(models.__all__) == 9


def test_uuid_primary_keys_are_used() -> None:
    for table in Base.metadata.tables.values():
        assert isinstance(table.c.id.type, Uuid)
        assert table.c.id.primary_key


def test_jsonb_is_limited_to_flexible_content() -> None:
    jsonb_columns = {
        f"{table.name}.{column.name}"
        for table in Base.metadata.tables.values()
        for column in table.columns
        if isinstance(column.type, JSONB)
    }
    assert jsonb_columns == {"content_blocks.content_json"}


def test_natural_key_constraints_are_present() -> None:
    assert Base.metadata.tables["users"].c.email.unique
    expected = {
        "newsletters": "uq_newsletter_source_url",
        "content_blocks": "uq_block_newsletter_position",
        "audio_segments": "uq_segment_audio_position",
        "playback_progress": "uq_progress_user_newsletter",
    }
    for table_name, constraint_name in expected.items():
        constraints = Base.metadata.tables[table_name].constraints
        assert any(
            isinstance(constraint, UniqueConstraint) and constraint.name == constraint_name
            for constraint in constraints
        )


def test_owned_foreign_keys_cascade_on_delete() -> None:
    cascade_foreign_keys = {
        "sources.user_id",
        "newsletters.source_id",
        "content_blocks.newsletter_id",
        "image_assets.content_block_id",
        "audio_assets.newsletter_id",
        "audio_segments.audio_asset_id",
        "ingestion_jobs.source_id",
        "playback_progress.user_id",
        "playback_progress.newsletter_id",
    }
    actual = {
        f"{table.name}.{foreign_key.parent.name}"
        for table in Base.metadata.tables.values()
        for foreign_key in table.foreign_keys
        if foreign_key.ondelete == "CASCADE"
    }
    assert cascade_foreign_keys <= actual


def test_regeneration_and_retry_rows_are_not_unique() -> None:
    assert not any(
        isinstance(constraint, UniqueConstraint)
        for constraint in Base.metadata.tables["audio_assets"].constraints
    )
    assert not any(
        isinstance(constraint, UniqueConstraint)
        for constraint in Base.metadata.tables["ingestion_jobs"].constraints
    )
