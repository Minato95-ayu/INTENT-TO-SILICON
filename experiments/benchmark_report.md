# NLP Engine Aggressive Benchmark Report (v2.0)

## Targets Evaluation
- **Target 1: OOV Rate < 5%** -> Actual: **0.0%** (Failures: 0/95)
- **Target 2: Pain Point Accuracy > 90%** -> Actual: **100.0%** (20/20)
- **Target 3: Avg Questions > 2.0** -> Actual: **2.29** (Total Qs: 218 / Inputs: 95)
- **Target 4: Negation Accuracy > 95%** -> Actual: **100.0%** (5/5)

## Detailed Logs
| Phrase | Type | Expected | Actual | Pass | Qs |
| --- | --- | --- | --- | --- | --- |
| paise kat gaye par order nahi hua | emotion | payment_anxiety | E:['payment_anxiety'] F:[] | ✅ | 2 |
| refund kab aayega bhai | emotion | payment_anxiety | E:['payment_anxiety'] F:[] | ✅ | 2 |
| account khali kar dega ye app | emotion | payment_anxiety | E:['payment_anxiety'] F:[] | ✅ | 2 |
| fraud ho gaya mere sath | emotion | payment_anxiety | E:['payment_anxiety'] F:[] | ✅ | 2 |
| double payment lag gaya | emotion | payment_anxiety | E:['payment_anxiety'] F:[] | ✅ | 2 |
| kaha click karu kuch samajh nahi aa raha | emotion | navigation_confusion | E:['navigation_confusion'] F:[] | ✅ | 2 |
| pata nahi aage kya karna hai confuse hu | emotion | navigation_confusion | E:['navigation_confusion'] F:[] | ✅ | 2 |
| sir ke upar se gaya ye interface | emotion | navigation_confusion | E:['navigation_confusion'] F:[] | ✅ | 2 |
| kuch dikh nahi raha | emotion | navigation_confusion | E:['navigation_confusion'] F:[] | ✅ | 2 |
| app hang ho gaya beech mein | emotion | performance_frustration | E:['performance_frustration'] F:[] | ✅ | 2 |
| safed screen aa gayi aur atak gaya | emotion | performance_frustration | E:['performance_frustration'] F:['security'] | ✅ | 1 |
| slow hai bekar app | emotion | performance_frustration | E:['performance_frustration'] F:[] | ✅ | 2 |
| kholte kholte subah ho jayegi | emotion | performance_frustration | E:['performance_frustration'] F:[] | ✅ | 2 |
| load nahi ho raha hai ghoom raha hai | emotion | performance_frustration | E:['performance_frustration'] F:[] | ✅ | 2 |
| data leak hone ka dar hai | emotion | trust_deficit | E:['trust_deficit'] F:['database'] | ✅ | 1 |
| safe nahi lag raha fraud hoga | emotion | trust_deficit | E:['trust_deficit'] F:[] | ✅ | 2 |
| mera data chori ho gaya toh? | emotion | trust_deficit | E:['trust_deficit'] F:['database'] | ✅ | 1 |
| customer care se baat karni hai koi nahi sunta | emotion | support_frustration | E:['support_frustration'] F:[] | ✅ | 2 |
| bot bakwas hai insaan se connect karo | emotion | support_frustration | E:['support_frustration'] F:[] | ✅ | 2 |
| koi sunne wala nahi hai | emotion | support_frustration | E:['support_frustration'] F:[] | ✅ | 2 |
| fast chahiye par chat nahi | negation | performance | Matched:['performance'] Negated:['realtime'] | ✅ | 3 |
| safe hona chahiye, bina live sync ke | negation | security | Matched:['security'] Negated:['realtime'] | ✅ | 2 |
| database chahiye lekin offline mat dena | negation | database | Matched:['database'] Negated:['availability'] | ✅ | 2 |
| speed chahiye par bina login ke | negation | performance | Matched:['performance'] Negated:['security'] | ✅ | 3 |
| scale acha ho, par data save mat karna | negation | scale | Matched:['scale'] Negated:['database'] | ✅ | 2 |
| mujhe pizza khana hai | oov | safe_halt | safe_halt (Expected) | ✅ | 0 |
| xyz123 random words hdjskd | oov | safe_halt | safe_halt (Expected) | ✅ | 0 |
| aaj mausam kaisa hai | oov | safe_halt | safe_halt (Expected) | ✅ | 0 |
| sachin tendulkar ne match jeeta | oov | safe_halt | safe_halt (Expected) | ✅ | 0 |
| I want to watch a movie on netflix | oov | safe_halt | safe_halt (Expected) | ✅ | 0 |
| sirf data theek karo | low_confidence | database | Matched:['database'] | ✅ | 2 |
| login banao | low_confidence | security | Matched:['security'] | ✅ | 2 |
| chat chahiye | low_confidence | realtime | Matched:['realtime'] | ✅ | 2 |
| fast speed loading chahiye 811 | functional | performance | Matched:['performance', 'scale'] | ✅ | 3 |
| bohot public aayegi server crash nahi hona chahiye 556 | functional | scale | Matched:['scale'] | ✅ | 2 |
| fast speed loading chahiye 331 | functional | performance | Matched:['performance', 'scale'] | ✅ | 3 |
| fast speed loading chahiye 23 | functional | performance | Matched:['performance', 'scale'] | ✅ | 3 |
| bohot public aayegi server crash nahi hona chahiye 987 | functional | scale | Matched:['scale'] | ✅ | 2 |
| offline bhi chalna chahiye 157 | functional | availability | Matched:['availability'] | ✅ | 2 |
| bohot public aayegi server crash nahi hona chahiye 783 | functional | scale | Matched:['scale'] | ✅ | 2 |
| realtime chat chahiye jismein speed achi ho 359 | functional | realtime | Matched:['realtime', 'performance'] | ✅ | 3 |
| fast speed loading chahiye 286 | functional | performance | Matched:['performance', 'scale'] | ✅ | 3 |
| offline bhi chalna chahiye 263 | functional | availability | Matched:['availability'] | ✅ | 2 |
| fast speed loading chahiye 609 | functional | performance | Matched:['performance', 'scale'] | ✅ | 3 |
| fast speed loading chahiye 826 | functional | performance | Matched:['performance', 'scale'] | ✅ | 3 |
| realtime chat chahiye jismein speed achi ho 466 | functional | realtime | Matched:['realtime', 'performance'] | ✅ | 3 |
| bohot public aayegi server crash nahi hona chahiye 575 | functional | scale | Matched:['scale'] | ✅ | 2 |
| offline bhi chalna chahiye 661 | functional | availability | Matched:['availability'] | ✅ | 2 |
| fast speed loading chahiye 357 | functional | performance | Matched:['performance', 'scale'] | ✅ | 3 |
| realtime chat chahiye jismein speed achi ho 41 | functional | realtime | Matched:['realtime', 'performance'] | ✅ | 3 |
| realtime chat chahiye jismein speed achi ho 19 | functional | realtime | Matched:['realtime', 'performance'] | ✅ | 3 |
| data database mein save hona chahiye security ke sath 346 | functional | database | Matched:['database', 'security'] | ✅ | 2 |
| realtime chat chahiye jismein speed achi ho 474 | functional | realtime | Matched:['realtime', 'performance'] | ✅ | 3 |
| data database mein save hona chahiye security ke sath 17 | functional | database | Matched:['database', 'security'] | ✅ | 2 |
| fast speed loading chahiye 942 | functional | performance | Matched:['performance', 'scale'] | ✅ | 3 |
| data database mein save hona chahiye security ke sath 682 | functional | database | Matched:['database', 'security'] | ✅ | 2 |
| fast speed loading chahiye 660 | functional | performance | Matched:['performance', 'scale'] | ✅ | 3 |
| data database mein save hona chahiye security ke sath 85 | functional | database | Matched:['database', 'security'] | ✅ | 2 |
| data database mein save hona chahiye security ke sath 780 | functional | database | Matched:['database', 'security'] | ✅ | 2 |
| realtime chat chahiye jismein speed achi ho 544 | functional | realtime | Matched:['realtime', 'performance'] | ✅ | 3 |
| bohot public aayegi server crash nahi hona chahiye 995 | functional | scale | Matched:['scale'] | ✅ | 2 |
| offline bhi chalna chahiye 446 | functional | availability | Matched:['availability'] | ✅ | 2 |
| realtime chat chahiye jismein speed achi ho 947 | functional | realtime | Matched:['realtime', 'performance'] | ✅ | 3 |
| offline bhi chalna chahiye 32 | functional | availability | Matched:['availability'] | ✅ | 2 |
| realtime chat chahiye jismein speed achi ho 971 | functional | realtime | Matched:['realtime', 'performance'] | ✅ | 3 |
| bohot public aayegi server crash nahi hona chahiye 211 | functional | scale | Matched:['scale'] | ✅ | 2 |
| data database mein save hona chahiye security ke sath 819 | functional | database | Matched:['database', 'security'] | ✅ | 2 |
| data database mein save hona chahiye security ke sath 261 | functional | database | Matched:['database', 'security'] | ✅ | 2 |
| data database mein save hona chahiye security ke sath 882 | functional | database | Matched:['database', 'security'] | ✅ | 2 |
| realtime chat chahiye jismein speed achi ho 868 | functional | realtime | Matched:['realtime', 'performance'] | ✅ | 3 |
| fast speed loading chahiye 537 | functional | performance | Matched:['performance', 'scale'] | ✅ | 3 |
| data database mein save hona chahiye security ke sath 287 | functional | database | Matched:['database', 'security'] | ✅ | 2 |
| bohot public aayegi server crash nahi hona chahiye 555 | functional | scale | Matched:['scale'] | ✅ | 2 |
| data database mein save hona chahiye security ke sath 579 | functional | database | Matched:['database', 'security'] | ✅ | 2 |
| fast speed loading chahiye 594 | functional | performance | Matched:['performance', 'scale'] | ✅ | 3 |
| bohot public aayegi server crash nahi hona chahiye 572 | functional | scale | Matched:['scale'] | ✅ | 2 |
| fast speed loading chahiye 102 | functional | performance | Matched:['performance', 'scale'] | ✅ | 3 |
| fast speed loading chahiye 391 | functional | performance | Matched:['performance', 'scale'] | ✅ | 3 |
| data database mein save hona chahiye security ke sath 737 | functional | database | Matched:['database', 'security'] | ✅ | 2 |
| realtime chat chahiye jismein speed achi ho 43 | functional | realtime | Matched:['realtime', 'performance'] | ✅ | 3 |
| realtime chat chahiye jismein speed achi ho 307 | functional | realtime | Matched:['realtime', 'performance'] | ✅ | 3 |
| data database mein save hona chahiye security ke sath 772 | functional | database | Matched:['database', 'security'] | ✅ | 2 |
| data database mein save hona chahiye security ke sath 441 | functional | database | Matched:['database', 'security'] | ✅ | 2 |
| bohot public aayegi server crash nahi hona chahiye 81 | functional | scale | Matched:['scale'] | ✅ | 2 |
| bohot public aayegi server crash nahi hona chahiye 762 | functional | scale | Matched:['scale'] | ✅ | 2 |
| data database mein save hona chahiye security ke sath 945 | functional | database | Matched:['database', 'security'] | ✅ | 2 |
| data database mein save hona chahiye security ke sath 564 | functional | database | Matched:['database', 'security'] | ✅ | 2 |
| bohot public aayegi server crash nahi hona chahiye 157 | functional | scale | Matched:['scale'] | ✅ | 2 |
| offline bhi chalna chahiye 890 | functional | availability | Matched:['availability'] | ✅ | 2 |
| realtime chat chahiye jismein speed achi ho 700 | functional | realtime | Matched:['realtime', 'performance'] | ✅ | 3 |
| fast speed loading chahiye 583 | functional | performance | Matched:['performance', 'scale'] | ✅ | 3 |
| fast speed loading chahiye 913 | functional | performance | Matched:['performance', 'scale'] | ✅ | 3 |
| data database mein save hona chahiye security ke sath 615 | functional | database | Matched:['database', 'security'] | ✅ | 2 |
| bohot public aayegi server crash nahi hona chahiye 415 | functional | scale | Matched:['scale'] | ✅ | 2 |
| bohot public aayegi server crash nahi hona chahiye 199 | functional | scale | Matched:['scale'] | ✅ | 2 |
| bohot public aayegi server crash nahi hona chahiye 327 | functional | scale | Matched:['scale'] | ✅ | 2 |
| offline bhi chalna chahiye 958 | functional | availability | Matched:['availability'] | ✅ | 2 |
| realtime chat chahiye jismein speed achi ho 908 | functional | realtime | Matched:['realtime', 'performance'] | ✅ | 3 |
| realtime chat chahiye jismein speed achi ho 243 | functional | realtime | Matched:['realtime', 'performance'] | ✅ | 3 |
| bohot public aayegi server crash nahi hona chahiye 808 | functional | scale | Matched:['scale'] | ✅ | 2 |
