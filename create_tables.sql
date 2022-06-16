DROP TABLE IF EXISTS  projects CASCADE;
DROP TABLE IF EXISTS  category CASCADE;
DROP TABLE IF EXISTS  creator CASCADE;
DROP TABLE IF EXISTS  location CASCADE;
DROP TABLE IF EXISTS  photo CASCADE;
DROP TABLE IF EXISTS  profile CASCADE;
DROP TABLE IF EXISTS  urls CASCADE;

CREATE TABLE projects(
    id                              INT PRIMARY KEY NOT NULL,
    backers_count                   INT,
    blurb                           TEXT,
    converted_pledged_amount        INT,
    country                         CHAR(2),
    country_displayable_name        VARCHAR(255),
    created_at                      INT,
    currency                        CHAR(3),
    currency_symbol                 VARCHAR(2),
    currency_trailing_code          BOOLEAN,
    current_currency                VARCHAR(255),
    deadline                        INT,
    disable_communication           BOOLEAN,
    fx_rate                         DECIMAL,
    goal                            DECIMAL,
    is_starrable                    BOOLEAN,
    launched_at                     INT,
    name                            TEXT,
    pledged                         DECIMAL,
    slug                            VARCHAR(255),
    source_url                      TEXT,
    spotlight                       BOOLEAN,
    staff_pick                      BOOLEAN,
    state                           VARCHAR(255),
    state_changed_at                INT,
    static_usd_rate                 DECIMAL,
    usd_exchange_rate               DECIMAL,
    usd_pledged                     DECIMAL,
    usd_type                        VARCHAR(255)
);

CREATE TABLE category(
    id                              INT,
    project_id                      INT NOT NULL,
    name                            VARCHAR(255),
    analytics_name                  VARCHAR(255),
    slug                            VARCHAR(255),
    position                        INT,
    parent_id                       INT,
    parent_name                     VARCHAR(255),
    color                           INT,
    "urls.web.discover"             TEXT,
    FOREIGN KEY (project_id) REFERENCES projects(id)
);

CREATE TABLE creator(
    id                              DECIMAL,
    project_id                      INT NOT NULL,
    name                            VARCHAR(255),
    slug                            VARCHAR(255),
    is_registered                   NUMERIC,
    is_email_verified               NUMERIC,
    chosen_currency                 NUMERIC,
    is_superbacker                  NUMERIC,
    "avatar.thumb"                  TEXT,
    "avatar.small"                  TEXT,
    "avatar.medium"                 TEXT,
    "urls.web.user"                 TEXT,
    "urls.api.user"                 TEXT,
    FOREIGN KEY (project_id) REFERENCES projects(id)
);

CREATE TABLE location(
    id                              DECIMAL,
    project_id                      INT NOT NULL,
    name                            VARCHAR(255),
    slug                            VARCHAR(255),
    short_name                      VARCHAR(255),
    displayable_name                VARCHAR(255),
    localized_name                  VARCHAR(255),
    country                         CHAR(2),
    state                           VARCHAR(255),
    type                            VARCHAR(255),
    is_root                         BOOLEAN,
    expanded_country                VARCHAR(255),
    "urls.web.discover"             TEXT,
    "urls.web.location"             TEXT,
    "urls.api.nearby_projects"      TEXT,
    FOREIGN KEY (project_id) REFERENCES projects(id)
);

CREATE TABLE photo(
    project_id                      INT NOT NULL,
    "key"                           TEXT,
    "full"                          TEXT,
    ed                              TEXT,
    med                             TEXT,
    little                          TEXT,
    small                           TEXT,
    thumb                           TEXT,
    "1024x576"                      TEXT,
    "1536x864"                      TEXT,
    FOREIGN KEY (project_id) REFERENCES projects(id)
);


CREATE TABLE profile(
    id                                                      DECIMAL,
    project_id                                              INT NOT NULL,
    state                                                   VARCHAR(255),
    state_changed_at                                        DECIMAL,
    name                                                    VARCHAR(255),
    blurb                                                   TEXT,
    background_color                                        VARCHAR(255),
    text_color                                              VARCHAR(255),
    link_background_color                                   VARCHAR(255),
    link_text_color                                         VARCHAR(255),
    link_text                                               VARCHAR(255),
    link_url                                                TEXT,
    show_feature_image                                      BOOLEAN,
    background_image_opacity                                DECIMAL,
    should_show_feature_image_section                       BOOLEAN,
    "feature_image_attributes.image_urls.default"           TEXT,
    "feature_image_attributes.image_urls.baseball_card"     TEXT,
    "feature_image_attributes.id"                           DECIMAL,
    "background_image_attributes.id"                        DECIMAL,
    "background_image_attributes.image_urls.default"        TEXT,
    "background_image_attributes.image_urls.baseball_card"  TEXT,
    FOREIGN KEY (project_id) REFERENCES projects(id)
);

CREATE TABLE urls(
    project_id                      INT NOT NULL,
    "web.project"                   TEXT,
    "web.rewards"                   TEXT,
    FOREIGN KEY (project_id) REFERENCES projects(id)
);
