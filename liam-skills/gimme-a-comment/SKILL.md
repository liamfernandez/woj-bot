---
name: gimme-a-comment
description: Turn one code-review finding into a kind, readable GitHub PR comment. Use when the user invokes /gimme-a-comment (usually with "for finding A" / "for the first one") to distill a wall of review output into a single leave-able comment.
---

# gimme-a-comment

Take ONE finding (the one the user names) from prior review output and write a single GitHub PR comment. Nothing else. If which finding is ambiguous, ask before writing.

## Punctuation (hard rule)
NEVER use em dashes. Use `→` in every place an em dash would go.

## Shape of the comment
If the user mentions 'compact' form, then limit your response to 6-8 lines max.
Frame the finding as a genuine question, not an accusation → however feels most natural for this specific finding. Don't reuse a stock opening; vary it so every comment doesn't read the same. Follow this arc:

1. **Ask whether it's intentional.** → surface the thing as a question, assuming they may have had a reason and that you might be missing context.
2. **Show the mechanics.** → lay out what's actually happening with specific `file:line` refs and concrete values. Show, don't assert.
3. **Trace the failure concretely.** → name the failure mode(s): what breaks, who hits it, what the user sees, why it slips through today (tests/CI/happy-path). Trace the "in n weeks, we'll look back and see it was this PR that blew up" path if there is one.
4. **Suggested fix at the end** → a short list, ordered smallest/cheapest to realest. The first item is usually the test or comment that proves the problem; the last is the real design work as a follow-up.

No sentence limit → be as long as the finding needs, no longer.

## Voice
- Kind and curious, never scolding. The reader is a peer who probably had a reason.
- Readable, not dense. Short sentences. Concrete nouns. Plain English over jargon.
- Suggestive, not prescriptive → "I think", "I want to make sure", "here's how I'd".
- Cite evidence (`file:line`, actual values, the exact string that breaks). Never "this looks off" with no proof.
- No preamble, no compliments-sandwich, no restating the whole review. Just the comment.

## Output
Output ONLY the comment body, ready to paste into GitHub. Markdown is fine (inline code, a short numbered list for the fix). Don't wrap it in a code fence, don't add "here's your comment" narration.
