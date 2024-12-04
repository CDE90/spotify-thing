-- NOTE: postgresql database

-- Artists Table
CREATE TABLE artists (
    id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    external_urls JSONB,
    href TEXT
);

-- Albums Table
CREATE TABLE albums (
    id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    album_type VARCHAR(50),
    release_date DATE,
    total_tracks INTEGER,
    images JSONB,
    external_urls JSONB
);

-- Album Artists Relationship Table (for many-to-many relationship)
CREATE TABLE album_artists (
    album_id VARCHAR(255),
    artist_id VARCHAR(255),
    PRIMARY KEY (album_id, artist_id),
    FOREIGN KEY (album_id) REFERENCES albums(id),
    FOREIGN KEY (artist_id) REFERENCES artists(id)
);

-- Tracks Table
CREATE TABLE tracks (
    id VARCHAR(255) PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    album_id VARCHAR(255),
    duration_ms INTEGER,
    track_number INTEGER,
    is_explicit BOOLEAN,
    popularity INTEGER,
    uri VARCHAR(255),
    FOREIGN KEY (album_id) REFERENCES albums(id)
);

-- Track Artists Relationship Table (for many-to-many relationship)
CREATE TABLE track_artists (
    track_id VARCHAR(255),
    artist_id VARCHAR(255),
    PRIMARY KEY (track_id, artist_id),
    FOREIGN KEY (track_id) REFERENCES tracks(id),
    FOREIGN KEY (artist_id) REFERENCES artists(id)
);

-- Listening History Table
CREATE TABLE listening_history (
    id SERIAL PRIMARY KEY,
    track_id VARCHAR(255) NOT NULL,
    listened_at TIMESTAMP WITH TIME ZONE NOT NULL DEFAULT NOW(),
    progress_ms INTEGER,
    context_type VARCHAR(50),
    context_uri VARCHAR(255),
    device_name VARCHAR(255),
    device_type VARCHAR(50),
    FOREIGN KEY (track_id) REFERENCES tracks(id)
);

-- Indexes for performance
CREATE INDEX idx_listening_history_track_id ON listening_history(track_id);
CREATE INDEX idx_listening_history_listened_at ON listening_history(listened_at);
CREATE INDEX idx_track_artists_track_id ON track_artists(track_id);
CREATE INDEX idx_track_artists_artist_id ON track_artists(artist_id);
