-- Artists CRUD

-- name: CreateArtist :one
INSERT INTO artists (
  id, name, external_urls, href
) VALUES (
  $1, $2, $3, $4
)
RETURNING *;

-- name: GetArtist :one
SELECT * FROM artists
WHERE id = $1 LIMIT 1;

-- name: ListArtists :many
SELECT * FROM artists
ORDER BY name;

-- name: UpdateArtist :exec
UPDATE artists
SET 
  name = $2,
  external_urls = $3,
  href = $4
WHERE id = $1;

-- name: DeleteArtist :exec
DELETE FROM artists
WHERE id = $1;

-- Albums CRUD

-- name: CreateAlbum :one
INSERT INTO albums (
  id, name, album_type, release_date, 
  total_tracks, images, external_urls
) VALUES (
  $1, $2, $3, $4, $5, $6, $7
)
RETURNING *;

-- name: GetAlbum :one
SELECT * FROM albums
WHERE id = $1 LIMIT 1;

-- name: ListAlbums :many
SELECT * FROM albums
ORDER BY release_date DESC;

-- name: UpdateAlbum :exec
UPDATE albums
SET 
  name = $2,
  album_type = $3,
  release_date = $4,
  total_tracks = $5,
  images = $6,
  external_urls = $7
WHERE id = $1;

-- name: DeleteAlbum :exec
DELETE FROM albums
WHERE id = $1;

-- Tracks CRUD

-- name: CreateTrack :one
INSERT INTO tracks (
  id, name, album_id, duration_ms, 
  track_number, is_explicit, popularity, uri
) VALUES (
  $1, $2, $3, $4, $5, $6, $7, $8
)
RETURNING *;

-- name: GetTrack :one
SELECT * FROM tracks
WHERE id = $1 LIMIT 1;

-- name: ListTracks :many
SELECT * FROM tracks
ORDER BY name;

-- name: UpdateTrack :exec
UPDATE tracks
SET 
  name = $2,
  album_id = $3,
  duration_ms = $4,
  track_number = $5,
  is_explicit = $6,
  popularity = $7,
  uri = $8
WHERE id = $1;

-- name: DeleteTrack :exec
DELETE FROM tracks
WHERE id = $1;

-- Listening History CRUD

-- name: CreateListeningHistory :one
INSERT INTO listening_history (
  track_id, listened_at, progress_ms, 
  context_type, context_uri, device_name, device_type
) VALUES (
  $1, $2, $3, $4, $5, $6, $7
)
RETURNING *;

-- name: GetListeningHistory :one
SELECT * FROM listening_history
WHERE id = $1 LIMIT 1;

-- name: ListListeningHistory :many
SELECT * FROM listening_history
ORDER BY listened_at DESC;

-- name: UpdateListeningHistory :exec
UPDATE listening_history
SET 
  track_id = $2,
  listened_at = $3,
  progress_ms = $4,
  context_type = $5,
  context_uri = $6,
  device_name = $7,
  device_type = $8
WHERE id = $1;

-- name: DeleteListeningHistory :exec
DELETE FROM listening_history
WHERE id = $1;

-- Relationship Table Operations

-- name: AddArtistToTrack :exec
INSERT INTO track_artists (track_id, artist_id)
VALUES ($1, $2)
ON CONFLICT (track_id, artist_id) DO NOTHING;

-- name: AddArtistToAlbum :exec
INSERT INTO album_artists (album_id, artist_id)
VALUES ($1, $2)
ON CONFLICT (album_id, artist_id) DO NOTHING;

-- name: DeleteTrackArtist :exec
DELETE FROM track_artists
WHERE track_id = $1 AND artist_id = $2;

-- name: DeleteAlbumArtist :exec
DELETE FROM album_artists
WHERE album_id = $1 AND artist_id = $2;
