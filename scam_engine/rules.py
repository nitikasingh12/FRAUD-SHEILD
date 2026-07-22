import re

RULES = {
    "impersonation": {
        "patterns": [
            r"\bcbi\b", r"\bed\b", r"\benforcement directorate\b",
            r"\bcustoms\b", r"\bincome tax department\b", r"\btrai\b",
            r"\bcyber ?crime cell\b", r"\bnarcotics\b", r"\bpolice\b",
            r"\brbi\b",
        ],
        "weight": 25,
        "label": "Claims to be a government or law enforcement authority",
    },
    "arrest_threat": {
        "patterns": [
            r"\bdigital arrest\b", r"\barrest warrant\b", r"\bunder arrest\b",
            r"\bwill be arrested\b", r"\blegal action\b", r"\bwarrant\b",
        ],
        "weight": 25,
        "label": "Threatens arrest or legal action",
    },
    "isolation_control": {
        "patterns": [
            r"do not disconnect", r"do not hang up", r"stay on (this|the) call",
            r"do not tell anyone", r"keep this call active",
            r"remain on video call", r"do not switch off",
        ],
        "weight": 20,
        "label": "Tries to isolate you or keep you on the call",
    },
    "urgency": {
        "patterns": [
            r"immediately", r"within \d+ (minutes|hours)", r"right now",
            r"final notice", r"last warning", r"before it'?s too late",
        ],
        "weight": 10,
        "label": "Creates artificial urgency",
    },
    "money_or_credentials_request": {
        "patterns": [
            r"(share|tell|give|read out|provide|enter).{0,15}(your |the |us )?(otp|upi pin|cvv|password|net ?banking)",
            r"transfer.*(account|amount|rupees|rs\.?)",
            r"share your (bank|account|card|aadhaar|pan|password|net ?banking)",
            r"pay the (fine|fee)",
            r"verification account",
        ],
        "weight": 20,
        "label": "Asks for money, OTP, or sensitive credentials",
    },
}

NEGATION_PATTERNS = [
    r"do not share", r"don'?t share", r"never share", r"please do not share",
]


def evaluate_rules(text: str):
    text_lower = text.lower()
    score = 0
    matched = []

    has_negation = any(re.search(p, text_lower) for p in NEGATION_PATTERNS)

    for name, rule in RULES.items():
        if name == "money_or_credentials_request" and has_negation:
            continue
        for pattern in rule["patterns"]:
            if re.search(pattern, text_lower):
                score += rule["weight"]
                matched.append(rule["label"])
                break

    return min(score, 100), matched