create table django_migrations
(
    id      integer generated by default as identity
        constraint django_migrations_pkey
        primary key,
    app     varchar(255) not null,
    name    varchar(255) not null,
    applied timestamp with time zone not null
);

alter table django_migrations owner to postgres;

create table account
(
    id          integer generated by default as identity
        constraint account_pkey
        primary key,
    username    varchar(100) not null
        constraint account_username_key
        unique,
    nickname    varchar(100) not null,
    email       varchar(254),
    password    varchar(256) not null,
    department  varchar(128),
    is_active   boolean      not null,
    is_delete   boolean      not null,
    disk_limit  bigint
        constraint account_disk_limit_check
        check (disk_limit >= 0),
    used_disk   bigint       not null
        constraint account_used_disk_check
        check (used_disk >= 0),
    create_time timestamp with time zone not null,
    update_time timestamp with time zone not null,
    parent_id   integer
        constraint account_parent_id_5f9163e3_fk_account_id
        references account
        deferrable initially deferred
);

alter table account owner to postgres;

create index account_username_cfe70fab_like
    on account (username varchar_pattern_ops);

create index account_parent_id_5f9163e3
    on account (parent_id);

create table django_content_type
(
    id        integer generated by default as identity
        constraint django_content_type_pkey
        primary key,
    app_label varchar(100) not null,
    model     varchar(100) not null,
    constraint django_content_type_app_label_model_76bd3d3b_uniq
        unique (app_label, model)
);

alter table django_content_type owner to postgres;

create table auth_permission
(
    id              integer generated by default as identity
        constraint auth_permission_pkey
        primary key,
    name            varchar(255) not null,
    content_type_id integer      not null
        constraint auth_permission_content_type_id_2f476e4b_fk_django_co
        references django_content_type
        deferrable initially deferred,
    codename        varchar(100) not null,
    constraint auth_permission_content_type_id_codename_01ab375a_uniq
        unique (content_type_id, codename)
);

alter table auth_permission owner to postgres;

create index auth_permission_content_type_id_2f476e4b
    on auth_permission (content_type_id);

create table auth_group
(
    id   integer generated by default as identity
        constraint auth_group_pkey
        primary key,
    name varchar(150) not null
        constraint auth_group_name_key
        unique
);

alter table auth_group owner to postgres;

create index auth_group_name_a6ea08ec_like
    on auth_group (name varchar_pattern_ops);

create table auth_group_permissions
(
    id            integer generated by default as identity
        constraint auth_group_permissions_pkey
        primary key,
    group_id      integer not null
        constraint auth_group_permissions_group_id_b120cbf9_fk_auth_group_id
        references auth_group
        deferrable initially deferred,
    permission_id integer not null
        constraint auth_group_permissio_permission_id_84c5c92e_fk_auth_perm
        references auth_permission
        deferrable initially deferred,
    constraint auth_group_permissions_group_id_permission_id_0cd325b0_uniq
        unique (group_id, permission_id)
);

alter table auth_group_permissions owner to postgres;

create index auth_group_permissions_group_id_b120cbf9
    on auth_group_permissions (group_id);

create index auth_group_permissions_permission_id_84c5c92e
    on auth_group_permissions (permission_id);

create table auth_user
(
    id           integer generated by default as identity
        constraint auth_user_pkey
        primary key,
    password     varchar(128) not null,
    last_login   timestamp with time zone,
    is_superuser boolean      not null,
    username     varchar(150) not null
        constraint auth_user_username_key
        unique,
    first_name   varchar(150) not null,
    last_name    varchar(150) not null,
    email        varchar(254) not null,
    is_staff     boolean      not null,
    is_active    boolean      not null,
    date_joined  timestamp with time zone not null
);

alter table auth_user owner to postgres;

create index auth_user_username_6821ab7c_like
    on auth_user (username varchar_pattern_ops);

create table auth_user_groups
(
    id       integer generated by default as identity
        constraint auth_user_groups_pkey
        primary key,
    user_id  integer not null
        constraint auth_user_groups_user_id_6a12ed8b_fk_auth_user_id
        references auth_user
        deferrable initially deferred,
    group_id integer not null
        constraint auth_user_groups_group_id_97559544_fk_auth_group_id
        references auth_group
        deferrable initially deferred,
    constraint auth_user_groups_user_id_group_id_94350c0c_uniq
        unique (user_id, group_id)
);

alter table auth_user_groups owner to postgres;

create index auth_user_groups_user_id_6a12ed8b
    on auth_user_groups (user_id);

create index auth_user_groups_group_id_97559544
    on auth_user_groups (group_id);

create table auth_user_user_permissions
(
    id            integer generated by default as identity
        constraint auth_user_user_permissions_pkey
        primary key,
    user_id       integer not null
        constraint auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id
        references auth_user
        deferrable initially deferred,
    permission_id integer not null
        constraint auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm
        references auth_permission
        deferrable initially deferred,
    constraint auth_user_user_permissions_user_id_permission_id_14a6b632_uniq
        unique (user_id, permission_id)
);

alter table auth_user_user_permissions owner to postgres;

create index auth_user_user_permissions_user_id_a95ead1b
    on auth_user_user_permissions (user_id);

create index auth_user_user_permissions_permission_id_1fbb5f2c
    on auth_user_user_permissions (permission_id);

create table django_admin_log
(
    id              integer generated by default as identity
        constraint django_admin_log_pkey
        primary key,
    action_time     timestamp with time zone not null,
    object_id       text,
    object_repr     varchar(200) not null,
    action_flag     smallint     not null
        constraint django_admin_log_action_flag_check
        check (action_flag >= 0),
    change_message  text         not null,
    content_type_id integer
        constraint django_admin_log_content_type_id_c4bce8eb_fk_django_co
        references django_content_type
        deferrable initially deferred,
    user_id         integer      not null
        constraint django_admin_log_user_id_c564eba6_fk_auth_user_id
        references auth_user
        deferrable initially deferred
);

alter table django_admin_log owner to postgres;

create index django_admin_log_content_type_id_c4bce8eb
    on django_admin_log (content_type_id);

create index django_admin_log_user_id_c564eba6
    on django_admin_log (user_id);

create table appearance_sitelayout
(
    id          bigint generated by default as identity
        constraint appearance_sitelayout_pkey
        primary key,
    title       varchar(64) not null,
    image       text        not null,
    create_time timestamp with time zone not null,
    update_time timestamp with time zone not null
);

alter table appearance_sitelayout owner to postgres;

create table config
(
    create_time timestamp with time zone not null,
    id          integer generated by default as identity
        constraint config_pkey
        primary key,
    name        varchar(100) not null
        constraint config_name_key
        unique,
    value       double precision,
    update_time timestamp with time zone not null,
    used        double precision
);

alter table config owner to postgres;

create index config_name_925d29d4_like
    on config (name varchar_pattern_ops);

create table flow
(
    id                        integer generated by default as identity
        constraint flow_pkey
        primary key,
    name                      varchar(100)  not null
        constraint flow_name_key
        unique,
    code                      varchar(128)  not null
        constraint flow_code_key
        unique,
    desp                      text          not null,
    owner_id                  bigint        not null,
    create_time               timestamp with time zone not null,
    update_time               timestamp with time zone not null,
    tar_path                  varchar(1024) not null,
    image_name                varchar(128)  not null
        constraint flow_image_name_key
        unique,
    alignment_tool            varchar(64)   not null,
    parameter_schema          text          not null,
    memory                    bigint        not null,
    sample_type               varchar(64)   not null,
    flow_type                 varchar(64)   not null,
    flow_category             varchar(64)   not null,
    allow_nonstandard_samples boolean       not null,
    details                   text          not null,
    panel_id                  integer
);

alter table flow owner to postgres;

create index flow_name_cd0b8935_like
    on flow (name varchar_pattern_ops);

create index flow_code_6d7bcfaa_like
    on flow (code varchar_pattern_ops);

create index flow_image_name_72ad481b_like
    on flow (image_name varchar_pattern_ops);

create index flow_panel_id_b4934503
    on flow (panel_id);

create table flow_samples
(
    id          integer generated by default as identity
        constraint flow_samples_pkey
        primary key,
    flow_id     bigint       not null,
    sample_id   bigint       not null,
    task_id     bigint       not null,
    project_id  bigint       not null,
    filepath    varchar(256) not null,
    create_time timestamp with time zone not null,
    update_time timestamp with time zone not null
);

alter table flow_samples owner to postgres;

create table flow_members
(
    id          integer generated by default as identity
        constraint flow_members_pkey
        primary key,
    create_time timestamp with time zone not null,
    account_id  integer not null
        constraint flow_members_account_id_77ff9db6_fk_account_id
        references account
        deferrable initially deferred,
    flow_id     integer not null
        constraint flow_members_flow_id_c9919511_fk_flow_id
        references flow
        deferrable initially deferred,
    constraint flow_members_account_id_flow_id_b94bacd0_uniq
        unique (account_id, flow_id)
);

alter table flow_members owner to postgres;

create index flow_members_account_id_77ff9db6
    on flow_members (account_id);

create index flow_members_flow_id_c9919511
    on flow_members (flow_id);

create table patient_patient
(
    id                 bigint generated by default as identity (maxvalue 2147483647)
        constraint patient_patient_pkey
        primary key,
    age                integer,
    birthday           date         not null,
    name               varchar(256),
    id_card            varchar(32)
        constraint patient_patient_id_card_key
        unique,
    medical_doctor     varchar(128),
    gender             varchar(12)  not null,
    location           varchar(256),
    identifier         varchar(256) not null
        constraint patient_patient_identifier_key
        unique,
    inspection_agency  varchar(256),
    tumor_stage        varchar(256),
    diagnosis          varchar(256),
    disease            varchar(256),
    family_history     varchar(256),
    medication_history varchar(256),
    treatment_history  varchar(256),
    create_time        timestamp with time zone not null,
    update_time        timestamp with time zone not null,
    creator_id         integer
        constraint patient_patient_creator_id_724ee032_fk_account_id
        references account
        deferrable initially deferred,
    recurrence_time    integer      not null,
    survival_time      integer      not null,
    blood_type         varchar(256),
    diagnosis_time     integer      not null,
    drinking           varchar(16)  not null,
    prognosis          varchar(512),
    smoking            varchar(16)  not null,
    viral_infection    varchar(16)  not null,
    prognosis_time     integer      not null
);

alter table patient_patient owner to postgres;

create index patient_patient_id_card_88572c0e_like
    on patient_patient (id_card varchar_pattern_ops);

create index patient_patient_identifier_ebf67de7_like
    on patient_patient (identifier varchar_pattern_ops);

create index patient_patient_creator_id_724ee032
    on patient_patient (creator_id);

create table samples
(
    id                 integer generated by default as identity
        constraint samples_pkey
        primary key,
    project_index      varchar(1024) not null,
    library_number     varchar(1024) not null,
    reagent_box        varchar(128)  not null,
    nucleic_break_type varchar(128)  not null,
    library_input      varchar(128)  not null,
    index_type         varchar(1024) not null,
    index_number       varchar(1024) not null,
    hybrid_input       varchar(1024) not null,
    risk               boolean       not null,
    nucleic_level      varchar(4)    not null,
    sample_identifier  varchar(256)  not null,
    identifier         varchar(256)  not null
        constraint samples_identifier_key
        unique,
    company            varchar(1024) not null,
    nucleic_type       varchar(16)   not null,
    fastq1_path        varchar(1024) not null,
    fastq2_path        varchar(1024) not null,
    user_id            bigint        not null,
    create_time        timestamp with time zone,
    modify_time        timestamp with time zone,
    sample_meta_id     integer
);

alter table samples owner to postgres;

create index samples_identifier_ffa74b89_like
    on samples (identifier varchar_pattern_ops);

create index samples_sample_meta_id_6bc95747
    on samples (sample_meta_id);

create table sample_meta
(
    id                 integer generated by default as identity
        constraint sample_meta_pkey
        primary key,
    sample_date        date             not null,
    test_date          date             not null,
    sample_componet    varchar(128)     not null,
    sample_type        varchar(128)     not null,
    panel_proportion   double precision not null,
    is_panel           boolean          not null,
    user_id            bigint           not null,
    patient_identifier varchar(256),
    identifier         varchar(256)     not null
        constraint sample_meta_identifier_key
        unique,
    create_time        timestamp with time zone,
    modify_time        timestamp with time zone,
    patient_id         bigint
);

alter table sample_meta owner to postgres;

create index sample_meta_identifier_f51b3557_like
    on sample_meta (identifier varchar_pattern_ops);

create index sample_meta_patient_id_25ef8ade
    on sample_meta (patient_id);

create table project
(
    id          integer generated by default as identity
        constraint project_pkey
        primary key,
    name        varchar(256) not null,
    "desc"      text         not null,
    is_visible  boolean      not null,
    is_builtin  boolean      not null,
    create_time timestamp with time zone not null,
    update_time timestamp with time zone not null,
    owner_id    integer      not null
        constraint project_owner_id_d7626fbc_fk_account_id
        references account
        deferrable initially deferred,
    parent_id   integer
        constraint project_parent_id_dc9b309f_fk_project_id
        references project
        deferrable initially deferred
);

alter table project owner to postgres;

create index project_owner_id_d7626fbc
    on project (owner_id);

create index project_parent_id_dc9b309f
    on project (parent_id);

create table project_members
(
    id          integer generated by default as identity
        constraint project_members_pkey
        primary key,
    create_time timestamp with time zone not null,
    account_id  integer not null
        constraint project_members_account_id_614aaea3_fk_account_id
        references account
        deferrable initially deferred,
    project_id  integer not null
        constraint project_members_project_id_bf2e42ec_fk_project_id
        references project
        deferrable initially deferred
);

alter table project_members owner to postgres;

create index project_members_account_id_614aaea3
    on project_members (account_id);

create index project_members_project_id_bf2e42ec
    on project_members (project_id);

create table project_samples
(
    id         integer generated by default as identity
        constraint project_samples_pkey
        primary key,
    project_id integer not null
        constraint project_samples_project_id_cb886349_fk_project_id
        references project
        deferrable initially deferred,
    sample_id  integer not null
        constraint project_samples_sample_id_e93fff40_fk_samples_id
        references samples
        deferrable initially deferred,
    constraint project_samples_project_id_sample_id_312a8dd1_uniq
        unique (project_id, sample_id)
);

alter table project_samples owner to postgres;

create index project_samples_project_id_cb886349
    on project_samples (project_id);

create index project_samples_sample_id_e93fff40
    on project_samples (sample_id);

create table action
(
    id      integer generated by default as identity
        constraint action_pkey
        primary key,
    code    varchar(32) not null,
    caption varchar(32) not null
);

alter table action owner to postgres;

create table permission
(
    id    integer generated by default as identity
        constraint permission_pkey
        primary key,
    title varchar(32) not null,
    url   varchar(32) not null,
    alias varchar(32)
);

alter table permission owner to postgres;

create table permission2action
(
    id            integer generated by default as identity
        constraint permission2action_pkey
        primary key,
    args          text,
    kwargs        text,
    customer_func varchar(32),
    action_id     integer not null
        constraint permission2action_action_id_608214ef_fk_action_id
        references action
        deferrable initially deferred,
    parent_id     integer
        constraint permission2action_parent_id_b20b080f_fk_permission2action_id
        references permission2action
        deferrable initially deferred,
    permission_id integer not null
        constraint permission2action_permission_id_2086c758_fk_permission_id
        references permission
        deferrable initially deferred
);

alter table permission2action owner to postgres;

create index permission2action_action_id_608214ef
    on permission2action (action_id);

create index permission2action_parent_id_b20b080f
    on permission2action (parent_id);

create index permission2action_permission_id_2086c758
    on permission2action (permission_id);

create table role
(
    id   integer generated by default as identity
        constraint role_pkey
        primary key,
    code varchar(32) not null
);

alter table role owner to postgres;

create table role_permission2action
(
    id                   integer generated by default as identity
        constraint role_permission2action_pkey
        primary key,
    role_id              integer not null
        constraint role_permission2action_role_id_a4e29877_fk_role_id
        references role
        deferrable initially deferred,
    permission2action_id integer not null
        constraint role_permission2acti_permission2action_id_40e7e763_fk_permissio
        references permission2action
        deferrable initially deferred,
    constraint role_permission2action_role_id_permission2actio_c6840aa5_uniq
        unique (role_id, permission2action_id)
);

alter table role_permission2action owner to postgres;

create index role_permission2action_role_id_a4e29877
    on role_permission2action (role_id);

create index role_permission2action_permission2action_id_40e7e763
    on role_permission2action (permission2action_id);

create table user2role
(
    id      integer generated by default as identity
        constraint user2role_pkey
        primary key,
    role_id integer not null
        constraint user2role_role_id_89f40cb5_fk_role_id
        references role
        deferrable initially deferred,
    user_id integer not null
        constraint user2role_user_id_42b14a48_fk_account_id
        references account
        deferrable initially deferred
);

alter table user2role owner to postgres;

create index user2role_role_id_89f40cb5
    on user2role (role_id);

create index user2role_user_id_42b14a48
    on user2role (user_id);

create table resource_limit_resourcelimit
(
    id          bigint generated by default as identity
        constraint resource_limit_resourcelimit_pkey
        primary key,
    "limit"     integer     not null
        constraint resource_limit_resourcelimit_limit_check
        check ("limit" >= 0),
    limit_type  varchar(24) not null,
    "desc"      text        not null,
    create_time timestamp with time zone not null,
    update_time timestamp with time zone not null,
    creator_id  integer     not null
        constraint resource_limit_resourcelimit_creator_id_7d6c8519_fk_account_id
        references account
        deferrable initially deferred,
    user_id     integer     not null
        constraint resource_limit_resourcelimit_user_id_2098b039_fk_account_id
        references account
        deferrable initially deferred
);

alter table resource_limit_resourcelimit owner to postgres;

create index resource_limit_resourcelimit_creator_id_7d6c8519
    on resource_limit_resourcelimit (creator_id);

create index resource_limit_resourcelimit_user_id_2098b039
    on resource_limit_resourcelimit (user_id);

create table django_session
(
    session_key  varchar(40) not null
        constraint django_session_pkey
        primary key,
    session_data text        not null,
    expire_date  timestamp with time zone not null
);

alter table django_session owner to postgres;

create index django_session_session_key_c0390e0f_like
    on django_session (session_key varchar_pattern_ops);

create index django_session_expire_date_a5c62663
    on django_session (expire_date);

create table django_site
(
    id     integer generated by default as identity
        constraint django_site_pkey
        primary key,
    domain varchar(100) not null
        constraint django_site_domain_a2e37b91_uniq
        unique,
    name   varchar(50)  not null
);

alter table django_site owner to postgres;

create index django_site_domain_a2e37b91_like
    on django_site (domain varchar_pattern_ops);

create table task
(
    id            integer generated by default as identity
        constraint task_pkey
        primary key,
    name          varchar(100) not null,
    status        smallint     not null,
    progress      smallint     not null,
    pid           varchar(256),
    is_merge      boolean      not null,
    result_path   text,
    result_dir    varchar(120),
    keep_bam      boolean      not null,
    has_cleaned   boolean      not null,
    is_qc         boolean      not null,
    env jsonb,
    priority      smallint     not null,
    memory        bigint       not null,
    samples jsonb not null,
    parameter jsonb,
    error_message text,
    create_time   timestamp with time zone not null,
    update_time   timestamp with time zone not null,
    creator_id    integer      not null
        constraint task_creator_id_2cac31da_fk_account_id
        references account
        deferrable initially deferred,
    flow_id       integer      not null
        constraint task_flow_id_de38496a_fk_flow_id
        references flow
        deferrable initially deferred,
    project_id    integer      not null
        constraint task_project_id_963d6354_fk_project_id
        references project
        deferrable initially deferred,
    log           text
);

alter table task owner to postgres;

create index task_creator_id_2cac31da
    on task (creator_id);

create index task_flow_id_de38496a
    on task (flow_id);

create index task_project_id_963d6354
    on task (project_id);

create table panel_group
(
    id          integer generated by default as identity
        constraint panel_group_pkey
        primary key,
    name        varchar(100) not null
        constraint panel_group_name_key
        unique,
    desp        text         not null,
    sort        integer      not null,
    enabled     boolean      not null,
    create_time timestamp with time zone not null,
    update_time timestamp with time zone not null
);

alter table panel_group owner to postgres;

create index panel_group_name_0f31037b_like
    on panel_group (name varchar_pattern_ops);

create table panel
(
    id             integer generated by default as identity
        constraint panel_pkey
        primary key,
    name           varchar(100) not null
        constraint panel_name_key
        unique,
    enabled        boolean      not null,
    sort           integer      not null,
    desp           text         not null,
    detail         text         not null,
    create_time    timestamp with time zone not null,
    update_time    timestamp with time zone not null,
    panel_group_id integer
);

alter table panel owner to postgres;

create index panel_name_f4040b5d_like
    on panel (name varchar_pattern_ops);

create index panel_panel_group_id_a5bfab33
    on panel (panel_group_id);

create table resource
(
    id          integer generated by default as identity
        constraint resource_pkey
        primary key,
    name        varchar(100),
    value       double precision,
    typ         varchar(24) not null,
    day         date        not null,
    create_time timestamp with time zone not null,
    update_time timestamp with time zone not null
);

alter table resource owner to postgres;

create table report_report
(
    id          integer generated by default as identity
        constraint report_report_pkey
        primary key,
    query       text    not null,
    comment     text,
    creator_id  integer not null
        constraint report_report_creator_id_f92ed918_fk_account_id
        references account
        deferrable initially deferred,
    task_id     integer not null,
    create_time timestamp with time zone,
    report_path text,
    status      varchar(32)
);

alter table report_report owner to postgres;

create index report_report_creator_id_f92ed918
    on report_report (creator_id);

create index report_report_task_id_c2efe36c
    on report_report (task_id);
