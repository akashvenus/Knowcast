---
name: edge-case-detection
description: Use before planning or implementing any feature. Asks the user about edge cases for the problem, never assumes their answers, and builds the plan from their responses.
---

# Edge Case Detection

Never assume what the user wants. Ask first, then plan.

## Process
1. Restate the feature in one or two sentences to confirm understanding.
2. Ask the user: "What edge cases have you already thought about?" and WAIT for the answer.
3. Then go through the categories below and ask about every one that applies to this feature.
   Ask in small batches (3-5 questions at a time), not one giant list.
4. Give each question a short example so a junior developer understands what is being asked.
5. If the user says "I don't know" or skips one, do not pick for them. Present 2-3 options with
   trade-offs and ask them to choose. Mark it as an open decision until answered.
6. Only after the answers are collected, write the plan. Include a table:
   | Edge case | Decision (user's answer) | How the code handles it | Test that proves it |
7. If a user's answer reveals a new edge case, ask follow-ups.

## Categories to check
- **Input:** empty, missing, null, too long, wrong type, wrong encoding, malformed, duplicate.
- **Size and limits:** huge files, huge responses, many items, zero items, rate limits, timeouts.
- **External services:** down, slow, returns garbage, changes format, partial success, quota exhausted.
- **Failure and recovery:** crash mid-way, retry, running twice, half-finished state, worker restart.
- **Concurrency:** two requests at once, same item processed twice, race conditions.
- **Security:** malicious URLs, unsafe files, unauthorized access, leaked secrets or logs.
- **Data:** ordering, missing optional fields, special characters, very old or future dates.
- **Operations:** what the user sees on failure, what gets logged, how to recover manually.

## Do not
- Do not decide for the user and then tell them afterward.
- Do not start coding until open decisions are resolved or explicitly deferred by the user.
- Do not skip this skill because a feature looks small.