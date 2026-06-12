import csv
import os
import random

base_dir = os.path.dirname(os.path.dirname(__file__))
dataset_path = os.path.join(base_dir, 'data', 'evaluation_dataset.csv')

functional = [
    "mujhe ek scalable app chahiye", "mera backend postgresql pe hona chahiye", 
    "ek fast system bana do jisme load balancer ho", "mujhe microservices architecture chahiye",
    "payment gateway add karna hai", "database bahut tagda hona chahiye",
    "lakhon log aayenge toh scale ho jaye", "otp login system lagana hai",
    "cloud pe deploy karna hai fast", "api architecture banana hai",
    "mujhe serverless framework use karna hai", "high speed data processing chahiye",
    "bheed aane par crash na ho aisi app", "docker container mein chalaunga",
    "ekdm solid database architecture chahiye", "realtime chat banana hai",
    "graphql use karna hai mujhe", "mujhe ek ai chatbot banana hai",
    "mujhe redis cache use karna hai", "log in security system banao",
    "payment gateway integrate kar do", "mujhe video streaming banana hai",
    "data backup automatically hona chahiye", "fastest database use karna hai",
    "mujhe scalable backend chahiye next js ke sath"
]

ambiguous = [
    "accha app bana do", "ek professional website chahiye", "modern design ho meri site ka",
    "kuch badhiya sa bana ke dikhao", "aisa system jo sabse alag ho",
    "ek naya startup idea hai", "beautiful UI chahiye", "mera system sabko pasand aaye",
    "ekdam mast application bana do", "world class software chahiye",
    "simple par badhiya ho", "design ekdum premium lagna chahiye",
    "aisa app jo sab download karein", "future ready app banao",
    "best tech stack use karo", "ekdum next level system",
    "mujhe ek app banani hai bas", "aisa website ho jo viral ho jaye",
    "sabse sundar app chahiye", "kuch naya try karna hai",
    "ek idea hai app banane ka", "startup ke liye app chahiye",
    "kisi ko pata na chale aisa app", "ekdam unique concept hai",
    "mujhe internet par business karna hai"
]

emotional = [
    "users ko trust feel hona chahiye", "log payment se darte hain",
    "customer ko confusion nahi honi chahiye", "bohot urgency hoti hai logo ko",
    "log bore ho jate hain mazza aana chahiye", "mujhe dar hai data chori na ho",
    "aisa app jo logo ko uljhan mein na daale", "logon ka time bache aur jaldi kaam ho",
    "ekdum private aur safe feel ho", "log pareshan na ho use karte waqt",
    "privacy bohot zaruri hai meri community ke liye", "users bahut impatient hote hain",
    "khushi milni chahiye app use karke", "logon ka data chori hone ka dar hai",
    "mujhe fraud se bachna hai", "users confuse ho ke app na chhod dein",
    "ekdum fun app banana hai", "mera idea kisi ko pata na chale",
    "users ko safe environment chahiye", "log scam se darte hain",
    "mera data leak nahi hona chahiye", "fast fast sab kaam ho jana chahiye",
    "app open karte hi maza aa jaye", "logon ko dhokha na mile",
    "bohot hi nizi aur akele ke liye app chahiye"
]

mixed = [
    "mujhe secure aur fast payment app chahiye lekin login simple hona chahiye",
    "app scalable ho par logon ko uljhan na ho use karne me",
    "database solid ho aur log bore na ho app mein",
    "urgency wali app chahiye jisme payment secure ho",
    "logon ko trust aaye aur app 10 lakh traffic sambhal le",
    "scalable architecture ho jisme data chori hone ka dar na ho",
    "fast app ho par privacy ekdum premium honi chahiye",
    "payment portal banana hai par log dhoke se darte hain",
    "app jaldi open ho aur mazza aaye chalane me",
    "ekdum simple UI ho taaki confuse na ho, par backend heavy ho",
    "database scalable chahiye aur app ekdum fun honi chahiye",
    "mera data private rahe aur scaling apne aap ho",
    "log pareshan na ho par security 2FA wali ho",
    "kuch bhi ho app secure honi chahiye fraud ke against",
    "aisa backend banao jo fraud roke aur jaldi chale",
    "khush hokar log use karein aur load balancer handle kare",
    "impatient users ke liye fast scalable app",
    "log scam se bachen aur backend AWS pe ho",
    "fun app jisme lakhon traffic aaye",
    "confusion na ho isliye guided onboarding do",
    "urgency ke liye guest login ho aur system fast ho",
    "trust build ho aur microservices use karein",
    "privacy toggle do aur backend scalable ho",
    "log uljhan mein na padein aur payment secure ho",
    "ekdum private network jisme traffic sambhalne ki takat ho"
]

with open(dataset_path, 'w', newline='', encoding='utf-8') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['id', 'input', 'category', 'source', 'expected_result'])
    
    id_counter = 1
    
    # Process functional
    for text in functional:
        writer.writerow([id_counter, text, "functional", "synthetic", "success"])
        id_counter += 1
        
    # Process ambiguous
    for text in ambiguous:
        writer.writerow([id_counter, text, "ambiguous", "synthetic", "clarification_required"])
        id_counter += 1
        
    # Process emotional
    for text in emotional:
        writer.writerow([id_counter, text, "emotional", "synthetic", "success"])
        id_counter += 1
        
    # Process mixed
    for text in mixed:
        writer.writerow([id_counter, text, "mixed", "synthetic", "success"])
        id_counter += 1

print(f"Generated {id_counter-1} synthetic test cases successfully at {dataset_path}.")
