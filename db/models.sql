CREATE TABLE user_state (
  chat_id BIGINT PRIMARY KEY,
  state JSONB
);

CREATE TABLE appointments (
  id SERIAL PRIMARY KEY,
  chat_id BIGINT,
  service TEXT,
  date DATE,
  time TIME
);

