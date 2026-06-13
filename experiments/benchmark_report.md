# NLP Engine Benchmark Report (v0.9)

## Summary
- **Total Phrases Tested**: 28
- **Intent Recognition Accuracy**: 95.7% (22/23)
- **Safe Halt (OOV) Accuracy**: 80.0% (4/5)
- **Clarification Trigger Rate**: 22 times triggered correctly.

## Detailed Logs
| Phrase | Expected | Actual | Pass |
| --- | --- | --- | --- |
| paise kat gaye par order nahi hua | Payment Anxiety | ['Payment Anxiety'] | ✅ |
| refund kab aayega bhai | Payment Anxiety | ['Payment Anxiety'] | ✅ |
| account khali kar dega ye app | Payment Anxiety | fail_hard | ❌ |
| scam lag raha hai mereko | Payment Anxiety | ['Trust Deficit', 'Payment Anxiety'] | ✅ |
| gareeb bana dega mehenga hai | Payment Anxiety | ['Payment Anxiety'] | ✅ |
| kholte kholte subah ho jayegi | Performance Frustration | ['Performance Frustration'] | ✅ |
| app hang ho gaya beech mein | Performance Frustration | ['Performance Frustration'] | ✅ |
| safed screen aa gayi aur atak gaya | Performance Frustration | ['Performance Frustration'] | ✅ |
| slow hai bekar app | Performance Frustration | ['Performance Frustration'] | ✅ |
| load nahi ho raha hai ghoom raha hai | Performance Frustration | ['Performance Frustration'] | ✅ |
| kaha click karu kuch samajh nahi aa raha | Navigation / UI Confusion | ['Navigation / UI Confusion'] | ✅ |
| pata nahi aage kya karna hai confuse hu | Navigation / UI Confusion | ['Navigation / UI Confusion'] | ✅ |
| sir ke upar se gaya ye interface | Navigation / UI Confusion | ['Navigation / UI Confusion'] | ✅ |
| bohot bawasir UI hai | Navigation / UI Confusion | ['Navigation / UI Confusion'] | ✅ |
| uljhan ho rahi hai hard hai | Navigation / UI Confusion | ['Navigation / UI Confusion'] | ✅ |
| jaldi kar bhai time nahi hai | Urgency | ['Urgency'] | ✅ |
| fatafat checkout karna hai | Urgency | ['Urgency'] | ✅ |
| emergency mein turant kaam aana chahiye | Urgency | ['Urgency'] | ✅ |
| data leak hone ka dar hai | Trust Deficit | ['Trust Deficit'] | ✅ |
| safe nahi lag raha fraud hoga | Trust Deficit | ['Trust Deficit'] | ✅ |
| mera data chori ho gaya toh? | Trust Deficit | ['Trust Deficit'] | ✅ |
| customer care se baat karni hai koi nahi sunta | Support Frustration | ['Support Frustration'] | ✅ |
| bot bakwas hai insaan se connect karo | Support Frustration | ['Performance Frustration', 'Support Frustration'] | ✅ |
| mujhe pizza khana hai | safe_halt | fail_hard | ✅ |
| xyz123 random words hdjskd | safe_halt | fail_hard | ✅ |
| aaj mausam kaisa hai | safe_halt | fail_hard | ✅ |
| sachin tendulkar ne match jeeta | safe_halt | fail_hard | ✅ |
| I want to watch a movie on netflix | safe_halt | success | ❌ |
