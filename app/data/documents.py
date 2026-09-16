"""Small synthetic knowledge base for the RAG demo.

Each entry is a short "document" about a fictional product, Aurora Cloud
Storage. Using synthetic, self-contained text means the whole demo runs
with zero external API keys and zero network calls.
"""

DOCUMENTS = [
    {
        "doc_id": "pricing.md",
        "title": "Aurora Cloud Storage Pricing",
        "text": (
            "Aurora Cloud Storage offers three tiers: Free, Pro, and Team. "
            "The Free tier includes 5GB of storage and supports up to 2 "
            "collaborators. The Pro tier costs $9 per month and includes "
            "500GB of storage, versioned backups, and priority support. "
            "The Team tier costs $29 per month per five seats and adds "
            "shared workspaces, audit logs, and single sign-on (SSO)."
        ),
    },
    {
        "doc_id": "security.md",
        "title": "Aurora Cloud Storage Security",
        "text": (
            "All files in Aurora Cloud Storage are encrypted at rest using "
            "AES-256 and in transit using TLS 1.3. Team tier customers can "
            "enable single sign-on (SSO) via SAML. Aurora performs an "
            "annual third-party penetration test and publishes a summary "
            "report to customers on the Team and Pro tiers."
        ),
    },
    {
        "doc_id": "sync.md",
        "title": "Aurora Cloud Storage Sync Behavior",
        "text": (
            "The Aurora desktop client syncs changed files every 30 "
            "seconds when the app is active, and every 5 minutes in the "
            "background. Conflicting edits create a copy named "
            "'filename (conflicted copy).ext' rather than overwriting "
            "either version. Sync can be paused from the tray icon."
        ),
    },
    {
        "doc_id": "sharing.md",
        "title": "Aurora Cloud Storage Sharing & Permissions",
        "text": (
            "Files and folders can be shared via a link with view-only or "
            "edit permissions. Link expiration is available on the Pro and "
            "Team tiers. Team tier admins can restrict external sharing "
            "entirely through workspace-level policy settings."
        ),
    },
    {
        "doc_id": "limits.md",
        "title": "Aurora Cloud Storage Limits",
        "text": (
            "The maximum individual file size is 5GB on the Free tier and "
            "50GB on Pro and Team tiers. API requests are rate-limited to "
            "120 requests per minute per account. Exceeding the rate limit "
            "returns an HTTP 429 response with a Retry-After header."
        ),
    },
]
