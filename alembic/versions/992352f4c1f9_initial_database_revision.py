"""Initial database revision

Revision ID: 992352f4c1f9
Revises: 
Create Date: 2022-07-11 09:46:44.259371

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = "992352f4c1f9"
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "organization",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.PrimaryKeyConstraint("id"),
        sa.UniqueConstraint("name"),
    )
    op.create_table(
        "user",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.ForeignKeyConstraint(
            ["organization_id"], ["organization.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_user_organization_id"), "user", ["organization_id"], unique=False
    )
    op.create_table(
        "project",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("organization_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("tokenizer", sa.String(), nullable=True),
        sa.Column("tokenizer_blank", sa.String(), nullable=True),
        sa.Column("status", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), nullable=True),
        sa.ForeignKeyConstraint(["created_by"], ["user.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["organization_id"], ["organization.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_project_created_by"), "project", ["created_by"], unique=False
    )
    op.create_index(
        op.f("ix_project_organization_id"), "project", ["organization_id"], unique=False
    )
    op.create_table(
        "user_activity",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("activity", sa.JSON(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("from_backup", sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(["created_by"], ["user.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_user_activity_created_by"),
        "user_activity",
        ["created_by"],
        unique=False,
    )
    op.create_table(
        "attribute",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("project_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("data_type", sa.String(), nullable=True),
        sa.Column("is_primary_key", sa.Boolean(), nullable=True),
        sa.Column("relative_position", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["project_id"], ["project.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_attribute_project_id"), "attribute", ["project_id"], unique=False
    )
    op.create_table(
        "data_slice",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("project_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("filter_data", sa.JSON(), nullable=True),
        sa.Column("filter_raw", sa.JSON(), nullable=True),
        sa.Column("static", sa.Boolean(), nullable=True),
        sa.Column("count", sa.Integer(), nullable=True),
        sa.Column("count_sql", sa.String(), nullable=True),
        sa.Column("slice_type", sa.String(), nullable=True),
        sa.Column("info", sa.JSON(), nullable=True),
        sa.ForeignKeyConstraint(["created_by"], ["user.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["project_id"], ["project.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_data_slice_created_by"), "data_slice", ["created_by"], unique=False
    )
    op.create_index(
        op.f("ix_data_slice_project_id"), "data_slice", ["project_id"], unique=False
    )
    op.create_table(
        "embedding",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("project_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("custom", sa.Boolean(), nullable=True),
        sa.Column("type", sa.String(), nullable=True),
        sa.Column("state", sa.String(), nullable=True),
        sa.Column("similarity_threshold", sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(["project_id"], ["project.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_embedding_project_id"), "embedding", ["project_id"], unique=False
    )
    op.create_table(
        "knowledge_base",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("project_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(["project_id"], ["project.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_knowledge_base_project_id"),
        "knowledge_base",
        ["project_id"],
        unique=False,
    )
    op.create_table(
        "notification",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("project_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("type", sa.String(), nullable=True),
        sa.Column("level", sa.String(), nullable=True),
        sa.Column("message", sa.String(), nullable=True),
        sa.Column("important", sa.Boolean(), nullable=True),
        sa.Column("state", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["project_id"], ["project.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_notification_project_id"), "notification", ["project_id"], unique=False
    )
    op.create_index(
        op.f("ix_notification_user_id"), "notification", ["user_id"], unique=False
    )
    op.create_table(
        "record",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("project_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("data", sa.JSON(), nullable=True),
        sa.Column("category", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["project_id"], ["project.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_record_created_at"), "record", ["created_at"], unique=False
    )
    op.create_index(
        op.f("ix_record_project_id"), "record", ["project_id"], unique=False
    )
    op.create_table(
        "record_tokenization_task",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("project_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("type", sa.String(), nullable=True),
        sa.Column("state", sa.String(), nullable=True),
        sa.Column("progress", sa.Float(), nullable=True),
        sa.Column("workload", sa.Integer(), nullable=True),
        sa.Column("started_at", sa.DateTime(), nullable=True),
        sa.Column("finished_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(["project_id"], ["project.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_record_tokenization_task_project_id"),
        "record_tokenization_task",
        ["project_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_record_tokenization_task_user_id"),
        "record_tokenization_task",
        ["user_id"],
        unique=False,
    )
    op.create_table(
        "upload_task",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("project_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("user_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("state", sa.String(), nullable=True),
        sa.Column("progress", sa.Float(), nullable=True),
        sa.Column("started_at", sa.DateTime(), nullable=True),
        sa.Column("finished_at", sa.DateTime(), nullable=True),
        sa.Column("file_name", sa.String(), nullable=True),
        sa.Column("file_type", sa.String(), nullable=True),
        sa.Column("file_import_options", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(["project_id"], ["project.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["user_id"], ["user.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_upload_task_project_id"), "upload_task", ["project_id"], unique=False
    )
    op.create_index(
        op.f("ix_upload_task_user_id"), "upload_task", ["user_id"], unique=False
    )
    op.create_table(
        "user_sessions",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("project_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("id_sql_statement", sa.String(), nullable=True),
        sa.Column("count_sql_statement", sa.String(), nullable=True),
        sa.Column("last_count", sa.Integer(), nullable=True),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("session_record_ids", sa.JSON(), nullable=True),
        sa.Column("random_seed", sa.Float(), nullable=True),
        sa.Column("temp_session", sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(["created_by"], ["user.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["project_id"], ["project.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_user_sessions_created_by"),
        "user_sessions",
        ["created_by"],
        unique=False,
    )
    op.create_index(
        op.f("ix_user_sessions_project_id"),
        "user_sessions",
        ["project_id"],
        unique=False,
    )
    op.create_table(
        "weak_supervision_task",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("project_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("state", sa.String(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("finished_at", sa.DateTime(), nullable=True),
        sa.Column("selected_information_sources", sa.String(), nullable=True),
        sa.Column("selected_labeling_tasks", sa.String(), nullable=True),
        sa.Column("distinct_records", sa.Integer(), nullable=True),
        sa.Column("result_count", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["created_by"], ["user.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["project_id"], ["project.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_weak_supervision_task_created_by"),
        "weak_supervision_task",
        ["created_by"],
        unique=False,
    )
    op.create_index(
        op.f("ix_weak_supervision_task_project_id"),
        "weak_supervision_task",
        ["project_id"],
        unique=False,
    )
    op.create_table(
        "data_slice_record_association",
        sa.Column("data_slice_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("record_id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("project_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("outlier_score", sa.Float(), nullable=True),
        sa.ForeignKeyConstraint(
            ["data_slice_id"], ["data_slice.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(["project_id"], ["project.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["record_id"], ["record.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("data_slice_id", "record_id"),
    )
    op.create_index(
        op.f("ix_data_slice_record_association_project_id"),
        "data_slice_record_association",
        ["project_id"],
        unique=False,
    )
    op.create_table(
        "embedding_tensor",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("project_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("record_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("embedding_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("data", sa.JSON(), nullable=True),
        sa.ForeignKeyConstraint(["embedding_id"], ["embedding.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["project_id"], ["project.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["record_id"], ["record.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_embedding_tensor_embedding_id"),
        "embedding_tensor",
        ["embedding_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_embedding_tensor_project_id"),
        "embedding_tensor",
        ["project_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_embedding_tensor_record_id"),
        "embedding_tensor",
        ["record_id"],
        unique=False,
    )
    op.create_table(
        "knowledge_term",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("project_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("knowledge_base_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("value", sa.String(), nullable=True),
        sa.Column("comment", sa.String(), nullable=True),
        sa.Column("blacklisted", sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(
            ["knowledge_base_id"], ["knowledge_base.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(["project_id"], ["project.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_knowledge_term_knowledge_base_id"),
        "knowledge_term",
        ["knowledge_base_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_knowledge_term_project_id"),
        "knowledge_term",
        ["project_id"],
        unique=False,
    )
    op.create_table(
        "labeling_task",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("project_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("attribute_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("task_target", sa.String(), nullable=True),
        sa.Column("task_type", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(["attribute_id"], ["attribute.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["project_id"], ["project.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_labeling_task_project_id"),
        "labeling_task",
        ["project_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_labeling_task_attribute_id"),
        "labeling_task",
        ["attribute_id"],
        unique=False,
    )
    op.create_table(
        "record_attribute_token_statistics",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("project_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("record_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("attribute_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("num_token", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(["attribute_id"], ["attribute.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["project_id"], ["project.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["record_id"], ["record.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_record_attribute_token_statistics_attribute_id"),
        "record_attribute_token_statistics",
        ["attribute_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_record_attribute_token_statistics_project_id"),
        "record_attribute_token_statistics",
        ["project_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_record_attribute_token_statistics_record_id"),
        "record_attribute_token_statistics",
        ["record_id"],
        unique=False,
    )
    op.create_table(
        "record_tokenized",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("project_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("record_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("bytes", sa.LargeBinary(), nullable=True),
        sa.Column("columns", sa.ARRAY(sa.String()), nullable=True),
        sa.ForeignKeyConstraint(["project_id"], ["project.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["record_id"], ["record.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_record_tokenized_project_id"),
        "record_tokenized",
        ["project_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_record_tokenized_record_id"),
        "record_tokenized",
        ["record_id"],
        unique=False,
    )
    op.create_table(
        "information_source",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("project_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("labeling_task_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("type", sa.String(), nullable=True),
        sa.Column("return_type", sa.String(), nullable=True),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("description", sa.String(), nullable=True),
        sa.Column("source_code", sa.String(), nullable=True),
        sa.Column("is_selected", sa.Boolean(), nullable=True),
        sa.Column("version", sa.Integer(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), nullable=True),
        sa.ForeignKeyConstraint(["created_by"], ["user.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["labeling_task_id"], ["labeling_task.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(["project_id"], ["project.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_information_source_created_by"),
        "information_source",
        ["created_by"],
        unique=False,
    )
    op.create_index(
        op.f("ix_information_source_labeling_task_id"),
        "information_source",
        ["labeling_task_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_information_source_project_id"),
        "information_source",
        ["project_id"],
        unique=False,
    )
    op.create_table(
        "labeling_task_label",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("project_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("name", sa.String(), nullable=True),
        sa.Column("labeling_task_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("color", sa.String(), nullable=True),
        sa.Column("hotkey", sa.String(), nullable=True),
        sa.ForeignKeyConstraint(["created_by"], ["user.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["labeling_task_id"], ["labeling_task.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(["project_id"], ["project.id"], ondelete="CASCADE"),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_labeling_task_label_created_by"),
        "labeling_task_label",
        ["created_by"],
        unique=False,
    )
    op.create_index(
        op.f("ix_labeling_task_label_labeling_task_id"),
        "labeling_task_label",
        ["labeling_task_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_labeling_task_label_project_id"),
        "labeling_task_label",
        ["project_id"],
        unique=False,
    )
    op.create_table(
        "information_source_payload",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("project_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("source_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("state", sa.String(), nullable=True),
        sa.Column("progress", sa.Float(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("finished_at", sa.DateTime(), nullable=True),
        sa.Column("iteration", sa.Integer(), nullable=True),
        sa.Column("source_code", sa.String(), nullable=True),
        sa.Column("input_data", sa.JSON(), nullable=True),
        sa.Column("output_data", sa.JSON(), nullable=True),
        sa.Column("logs", sa.ARRAY(sa.String()), nullable=True),
        sa.ForeignKeyConstraint(["created_by"], ["user.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["project_id"], ["project.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["source_id"], ["information_source.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_information_source_payload_created_by"),
        "information_source_payload",
        ["created_by"],
        unique=False,
    )
    op.create_index(
        op.f("ix_information_source_payload_project_id"),
        "information_source_payload",
        ["project_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_information_source_payload_source_id"),
        "information_source_payload",
        ["source_id"],
        unique=False,
    )
    op.create_table(
        "information_source_statistics",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("project_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("source_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column(
            "labeling_task_label_id", postgresql.UUID(as_uuid=True), nullable=True
        ),
        sa.Column("true_positives", sa.Integer(), nullable=True),
        sa.Column("false_positives", sa.Integer(), nullable=True),
        sa.Column("false_negatives", sa.Integer(), nullable=True),
        sa.Column("record_coverage", sa.Integer(), nullable=True),
        sa.Column("total_hits", sa.Integer(), nullable=True),
        sa.Column("source_conflicts", sa.Integer(), nullable=True),
        sa.Column("source_overlaps", sa.Integer(), nullable=True),
        sa.ForeignKeyConstraint(
            ["labeling_task_label_id"], ["labeling_task_label.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(["project_id"], ["project.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["source_id"], ["information_source.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_information_source_statistics_labeling_task_label_id"),
        "information_source_statistics",
        ["labeling_task_label_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_information_source_statistics_project_id"),
        "information_source_statistics",
        ["project_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_information_source_statistics_source_id"),
        "information_source_statistics",
        ["source_id"],
        unique=False,
    )
    op.create_table(
        "information_source_statistics_exclusion",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("project_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("record_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("source_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.ForeignKeyConstraint(["project_id"], ["project.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["record_id"], ["record.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["source_id"], ["information_source.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_information_source_statistics_exclusion_project_id"),
        "information_source_statistics_exclusion",
        ["project_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_information_source_statistics_exclusion_record_id"),
        "information_source_statistics_exclusion",
        ["record_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_information_source_statistics_exclusion_source_id"),
        "information_source_statistics_exclusion",
        ["source_id"],
        unique=False,
    )
    op.create_table(
        "record_label_association",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("project_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("record_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column(
            "labeling_task_label_id", postgresql.UUID(as_uuid=True), nullable=True
        ),
        sa.Column("source_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("weak_supervision_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("source_type", sa.String(), nullable=True),
        sa.Column("return_type", sa.String(), nullable=True),
        sa.Column("confidence", sa.Float(), nullable=True),
        sa.Column("created_at", sa.DateTime(), nullable=True),
        sa.Column("created_by", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column("is_gold_star", sa.Boolean(), nullable=True),
        sa.Column("is_valid_manual_label", sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(["created_by"], ["user.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["labeling_task_label_id"], ["labeling_task_label.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(["project_id"], ["project.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(["record_id"], ["record.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["source_id"], ["information_source.id"], ondelete="CASCADE"
        ),
        sa.ForeignKeyConstraint(
            ["weak_supervision_id"], ["weak_supervision_task.id"], ondelete="CASCADE"
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_record_label_association_created_by"),
        "record_label_association",
        ["created_by"],
        unique=False,
    )
    op.create_index(
        op.f("ix_record_label_association_is_valid_manual_label"),
        "record_label_association",
        ["is_valid_manual_label"],
        unique=False,
    )
    op.create_index(
        op.f("ix_record_label_association_labeling_task_label_id"),
        "record_label_association",
        ["labeling_task_label_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_record_label_association_project_id"),
        "record_label_association",
        ["project_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_record_label_association_record_id"),
        "record_label_association",
        ["record_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_record_label_association_source_id"),
        "record_label_association",
        ["source_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_record_label_association_weak_supervision_id"),
        "record_label_association",
        ["weak_supervision_id"],
        unique=False,
    )
    op.create_table(
        "record_label_association_token",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("project_id", postgresql.UUID(as_uuid=True), nullable=True),
        sa.Column(
            "record_label_association_id", postgresql.UUID(as_uuid=True), nullable=True
        ),
        sa.Column("token_index", sa.Integer(), nullable=True),
        sa.Column("is_beginning_token", sa.Boolean(), nullable=True),
        sa.ForeignKeyConstraint(["project_id"], ["project.id"], ondelete="CASCADE"),
        sa.ForeignKeyConstraint(
            ["record_label_association_id"],
            ["record_label_association.id"],
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index(
        op.f("ix_record_label_association_token_project_id"),
        "record_label_association_token",
        ["project_id"],
        unique=False,
    )
    op.create_index(
        op.f("ix_record_label_association_token_record_label_association_id"),
        "record_label_association_token",
        ["record_label_association_id"],
        unique=False,
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(
        op.f("ix_record_label_association_token_record_label_association_id"),
        table_name="record_label_association_token",
    )
    op.drop_index(
        op.f("ix_record_label_association_token_project_id"),
        table_name="record_label_association_token",
    )
    op.drop_table("record_label_association_token")
    op.drop_index(
        op.f("ix_record_label_association_weak_supervision_id"),
        table_name="record_label_association",
    )
    op.drop_index(
        op.f("ix_record_label_association_source_id"),
        table_name="record_label_association",
    )
    op.drop_index(
        op.f("ix_record_label_association_record_id"),
        table_name="record_label_association",
    )
    op.drop_index(
        op.f("ix_record_label_association_project_id"),
        table_name="record_label_association",
    )
    op.drop_index(
        op.f("ix_record_label_association_labeling_task_label_id"),
        table_name="record_label_association",
    )
    op.drop_index(
        op.f("ix_record_label_association_is_valid_manual_label"),
        table_name="record_label_association",
    )
    op.drop_index(
        op.f("ix_record_label_association_created_by"),
        table_name="record_label_association",
    )
    op.drop_table("record_label_association")
    op.drop_index(
        op.f("ix_information_source_statistics_exclusion_source_id"),
        table_name="information_source_statistics_exclusion",
    )
    op.drop_index(
        op.f("ix_information_source_statistics_exclusion_record_id"),
        table_name="information_source_statistics_exclusion",
    )
    op.drop_index(
        op.f("ix_information_source_statistics_exclusion_project_id"),
        table_name="information_source_statistics_exclusion",
    )
    op.drop_table("information_source_statistics_exclusion")
    op.drop_index(
        op.f("ix_information_source_statistics_source_id"),
        table_name="information_source_statistics",
    )
    op.drop_index(
        op.f("ix_information_source_statistics_project_id"),
        table_name="information_source_statistics",
    )
    op.drop_index(
        op.f("ix_information_source_statistics_labeling_task_label_id"),
        table_name="information_source_statistics",
    )
    op.drop_table("information_source_statistics")
    op.drop_index(
        op.f("ix_information_source_payload_source_id"),
        table_name="information_source_payload",
    )
    op.drop_index(
        op.f("ix_information_source_payload_project_id"),
        table_name="information_source_payload",
    )
    op.drop_index(
        op.f("ix_information_source_payload_created_by"),
        table_name="information_source_payload",
    )
    op.drop_table("information_source_payload")
    op.drop_index(
        op.f("ix_labeling_task_label_project_id"), table_name="labeling_task_label"
    )
    op.drop_index(
        op.f("ix_labeling_task_label_labeling_task_id"),
        table_name="labeling_task_label",
    )
    op.drop_index(
        op.f("ix_labeling_task_label_created_by"), table_name="labeling_task_label"
    )
    op.drop_table("labeling_task_label")
    op.drop_index(
        op.f("ix_information_source_project_id"), table_name="information_source"
    )
    op.drop_index(
        op.f("ix_information_source_labeling_task_id"), table_name="information_source"
    )
    op.drop_index(
        op.f("ix_information_source_created_by"), table_name="information_source"
    )
    op.drop_table("information_source")
    op.drop_index(op.f("ix_record_tokenized_record_id"), table_name="record_tokenized")
    op.drop_index(op.f("ix_record_tokenized_project_id"), table_name="record_tokenized")
    op.drop_table("record_tokenized")
    op.drop_index(
        op.f("ix_record_attribute_token_statistics_record_id"),
        table_name="record_attribute_token_statistics",
    )
    op.drop_index(
        op.f("ix_record_attribute_token_statistics_project_id"),
        table_name="record_attribute_token_statistics",
    )
    op.drop_index(
        op.f("ix_record_attribute_token_statistics_attribute_id"),
        table_name="record_attribute_token_statistics",
    )
    op.drop_table("record_attribute_token_statistics")
    op.drop_index(op.f("ix_labeling_task_project_id"), table_name="labeling_task")
    op.drop_table("labeling_task")
    op.drop_index(op.f("ix_knowledge_term_project_id"), table_name="knowledge_term")
    op.drop_index(
        op.f("ix_knowledge_term_knowledge_base_id"), table_name="knowledge_term"
    )
    op.drop_table("knowledge_term")
    op.drop_index(op.f("ix_embedding_tensor_record_id"), table_name="embedding_tensor")
    op.drop_index(op.f("ix_embedding_tensor_project_id"), table_name="embedding_tensor")
    op.drop_index(
        op.f("ix_embedding_tensor_embedding_id"), table_name="embedding_tensor"
    )
    op.drop_table("embedding_tensor")
    op.drop_index(
        op.f("ix_data_slice_record_association_project_id"),
        table_name="data_slice_record_association",
    )
    op.drop_table("data_slice_record_association")
    op.drop_index(
        op.f("ix_weak_supervision_task_project_id"), table_name="weak_supervision_task"
    )
    op.drop_index(
        op.f("ix_weak_supervision_task_created_by"), table_name="weak_supervision_task"
    )
    op.drop_table("weak_supervision_task")
    op.drop_index(op.f("ix_user_sessions_project_id"), table_name="user_sessions")
    op.drop_index(op.f("ix_user_sessions_created_by"), table_name="user_sessions")
    op.drop_table("user_sessions")
    op.drop_index(op.f("ix_upload_task_user_id"), table_name="upload_task")
    op.drop_index(op.f("ix_upload_task_project_id"), table_name="upload_task")
    op.drop_table("upload_task")
    op.drop_index(
        op.f("ix_record_tokenization_task_user_id"),
        table_name="record_tokenization_task",
    )
    op.drop_index(
        op.f("ix_record_tokenization_task_project_id"),
        table_name="record_tokenization_task",
    )
    op.drop_table("record_tokenization_task")
    op.drop_index(op.f("ix_record_project_id"), table_name="record")
    op.drop_index(op.f("ix_record_created_at"), table_name="record")
    op.drop_table("record")
    op.drop_index(op.f("ix_notification_user_id"), table_name="notification")
    op.drop_index(op.f("ix_notification_project_id"), table_name="notification")
    op.drop_table("notification")
    op.drop_index(op.f("ix_knowledge_base_project_id"), table_name="knowledge_base")
    op.drop_table("knowledge_base")
    op.drop_index(op.f("ix_embedding_project_id"), table_name="embedding")
    op.drop_table("embedding")
    op.drop_index(op.f("ix_data_slice_project_id"), table_name="data_slice")
    op.drop_index(op.f("ix_data_slice_created_by"), table_name="data_slice")
    op.drop_table("data_slice")
    op.drop_index(op.f("ix_attribute_project_id"), table_name="attribute")
    op.drop_table("attribute")
    op.drop_index(op.f("ix_user_activity_created_by"), table_name="user_activity")
    op.drop_table("user_activity")
    op.drop_index(op.f("ix_project_organization_id"), table_name="project")
    op.drop_index(op.f("ix_project_created_by"), table_name="project")
    op.drop_table("project")
    op.drop_index(op.f("ix_user_organization_id"), table_name="user")
    op.drop_table("user")
    op.drop_table("organization")
    # ### end Alembic commands ###