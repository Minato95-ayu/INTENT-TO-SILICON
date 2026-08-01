import csv

prompts = [
    # Latency < 200ms
    ("Mera app bahot tezi se load hona chahiye", "Latency < 200ms"),
    ("Bina lag ke turant page khul jaye", "Latency < 200ms"),
    ("Jaldi reply aana mangta hai", "Latency < 200ms"),
    
    # AES-256 Encryption
    ("Koi bhi hack na kar paye mere data ko", "AES-256 Encryption"),
    ("Information secure rehni chahiye hamesha", "AES-256 Encryption"),
    ("Data leak ka risk zero hona chahiye", "AES-256 Encryption"),
    
    # Auto-scaling
    ("Kal ko lakhon log aayenge app par", "Auto-scaling"),
    ("Traffic badhne par server down nahi hona chahiye", "Auto-scaling"),
    ("Heavy load handle kar sake system", "Auto-scaling"),
    
    # RBAC / Admin Only
    ("Sirf mujhe hi backend dikhna chahiye", "RBAC / Admin Only"),
    ("Users ko admin section mat dikhana", "RBAC / Admin Only"),
    ("Kaun kya dekh sakta hai uspe control chahiye", "RBAC / Admin Only"),
    
    # Resource-constrained footprint
    ("App ka size bahot chhota rakhna hai", "Resource-constrained footprint"),
    ("Kam memory me chalne wala code likho", "Resource-constrained footprint"),
    ("Low end mobile pe bhi chal jana chahiye", "Resource-constrained footprint"),
    
    # WebSockets
    ("Jaise hi koi message kare instantly dikhna chahiye", "WebSockets"),
    ("Live chatting feature chahiye app me", "WebSockets"),
    ("Real time data sync hona zaroori hai", "WebSockets"),
    
    # Public Access
    ("Sab log bina account ke dekh sakein", "Public Access"),
    ("Koi OTP ya password nahi mangna hai", "Public Access"),
    ("Open for all rakhna hai isko", "Public Access"),
    
    # Offline Support
    ("Agar net chala jaye to bhi app kaam kare", "Offline Support"),
    ("Airplane mode me bhi details dikhe", "Offline Support"),
    ("No connection me data locally save ho jaye", "Offline Support"),
    
    # SQLite
    ("Sasta aur halka data store karke rakho", "SQLite"),
    ("Database ke liye zyada paise nahi kharchne", "SQLite"),
    ("Local DB me kaam chala lo", "SQLite"),
    
    # Admin Portal
    ("Mujhe sab manage karne ke liye ek panel de do", "Admin Portal"),
    ("Peeche se control karne ka setup banao", "Admin Portal"),
    ("Users aur sales track karne ke liye screen chahiye", "Admin Portal"),
    
    # Out of Distribution (Edge Cases)
    ("App ka color theme dark hona chahiye", "Unknown Specification"),
    ("SEO Google pe number one aana chahiye", "Unknown Specification"),
    ("Razorpay payment gateway laga dena", "Unknown Specification")
]

with open('dataset.csv', 'w', newline='', encoding='utf-8') as f:
    writer = csv.writer(f)
    writer.writerow(["Prompt", "Expected"])
    for p, e in prompts:
        writer.writerow([p, e])

print("Generated dataset.csv with 33 held-out testing prompts.")
