from scam_engine.rules import evaluate_rules
from scam_engine.classifier import predict_proba

REPORTING_INFO = (
    "Report this to the National Cyber Crime Reporting Portal at "
    "https://cybercrime.gov.in or call the Cyber Crime Helpline at 1930."
)


def assess(text: str) -> dict:
    rule_score, matched_categories = evaluate_rules(text)

    try:
        ml_proba = predict_proba(text)
    except FileNotFoundError:
        ml_proba = None

    if ml_proba is not None:
        combined = 0.5 * rule_score + 0.5 * (ml_proba * 100)
    else:
        combined = rule_score

    if combined >= 60:
        level = "High"
    elif combined >= 30:
        level = "Medium"
    else:
        level = "Low"

    response = build_response(level, matched_categories)

    return {
        "risk_level": level,
        "risk_score": round(combined, 1),
        "rule_score": rule_score,
        "ml_probability": round(ml_proba * 100, 1) if ml_proba is not None else None,
        "matched_categories": matched_categories,
        "response": response,
    }


def build_response(level: str, matched_categories: list) -> str:
    if level == "High":
        base = (
            "This message shows strong signs of a scam, possibly a digital arrest "
            "or impersonation attempt. Do not transfer money, share OTPs, or stay "
            "on the call. Hang up or stop replying now."
        )
    elif level == "Medium":
        base = (
            "This message has some characteristics of a scam. Be cautious, "
            "verify independently through official channels before taking any action, "
            "and never share OTPs or bank details over a call or message."
        )
    else:
        base = (
            "This message does not show strong scam indicators, but always stay "
            "cautious with unexpected requests for money or personal information."
        )

    if matched_categories:
        reasons = "; ".join(sorted(set(matched_categories)))
        base += f" Flagged reasons: {reasons}."

    if level in ("High", "Medium"):
        base += " " + REPORTING_INFO

    return base