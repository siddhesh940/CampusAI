"""
Application constants.
"""

# Document types accepted for upload
DOCUMENT_TYPES = [
    "id_proof",
    "marksheet_10th",
    "marksheet_12th",
    "graduation_marksheet",
    "photo",
    "medical_certificate",
    "transfer_certificate",
    "migration_certificate",
    "income_certificate",
    "caste_certificate",
    "address_proof",
    "other",
]

# Maximum file size for uploads (10 MB)
MAX_FILE_SIZE_MB = 10
MAX_FILE_SIZE_BYTES = MAX_FILE_SIZE_MB * 1024 * 1024

# Allowed MIME types for document uploads
ALLOWED_MIME_TYPES = [
    "application/pdf",
    "image/jpeg",
    "image/png",
    "image/webp",
]

# Default onboarding checklist items per category
DEFAULT_CHECKLIST = [
    {"title": "Complete Profile", "category": "profile", "order": 1, "is_required": True},
    {"title": "Upload ID Proof", "category": "documents", "order": 2, "is_required": True},
    {"title": "Upload Marksheets", "category": "documents", "order": 3, "is_required": True},
    {"title": "Upload Photo", "category": "documents", "order": 4, "is_required": True},
    {"title": "Upload Medical Certificate", "category": "documents", "order": 5, "is_required": False},
    {"title": "Pay Tuition Fees", "category": "payments", "order": 6, "is_required": True},
    {"title": "Pay Hostel Fees", "category": "payments", "order": 7, "is_required": False},
    {"title": "Apply for Hostel", "category": "hostel", "order": 8, "is_required": False},
    {"title": "Activate LMS Access", "category": "lms", "order": 9, "is_required": True},
    {"title": "Review Onboarding Guide", "category": "profile", "order": 10, "is_required": False},
]

# Payment types
PAYMENT_TYPES = [
    "tuition",
    "hostel",
    "library",
    "laboratory",
    "examination",
    "sports",
    "other",
]
