  -- testdb name = test
  CREATE TABLE users (
    email_id TEXT PRIMARY KEY,
    password TEXT,
    status INTEGER
  );

  CREATE TABLE position (
    position_id SERIAL PRIMARY KEY,
    position TEXT
  );

  CREATE TABLE election (
    election_id SERIAL PRIMARY KEY,
    start_datetime TIMESTAMP,
    end_datetime TIMESTAMP,
    admin_email TEXT REFERENCES users(email_id)
  );

  CREATE TABLE candidate (
    email_id TEXT PRIMARY KEY,
    name TEXT,
    votes INTEGER DEFAULT 0,
    position_id INTEGER REFERENCES position(position_id),
    election_id INTEGER REFERENCES election(election_id)
  );

  CREATE TABLE wins (
    candidate_email TEXT REFERENCES candidate(email_id),
    position_id INTEGER REFERENCES position(position_id)
  );

  CREATE TABLE votes_for (
    voter_email TEXT REFERENCES users(email_id),
    position_id INTEGER REFERENCES position(position_id)
  );

  -- insert dummy data into tables
  INSERT INTO users (email_id, password, status) VALUES ('hadif_b190513cs@nitc.ac.in', 'd30e375bd0da079acfecfe8206e21c62fc3136a35def934dce52150db4f3c135', -1);
  INSERT INTO users (email_id, password, status) VALUES ('hanna_b190420cs@nitc.ac.in', '086b42dd0491ea53914359b962dfe56dd17a1bcaaf9858ced0f9bccaef065d50', -1);
  INSERT INTO users (email_id, password, status) VALUES ('harimurali_b190547cs@nitc.ac.in', '8b0b28c15c2da3a92a41019d86aaa26328a76508dd80dfb87230fa878f3254c8', -1);
  INSERT INTO users (email_id, password, status) VALUES ('faseem_b190515cs@nitc.ac.in', 'd206c5d8b17a4f0d61b26641cc9bc2d4e3ccda4a8877d92158a1b43395b7471c', -1);
  INSERT INTO users (email_id, password, status) VALUES ('abhinav_b190461cs@nitc.ac.in', '86a8157869152c00b3a336aa148c1d8dd8e7c2c0a2fa2b6177ccfcaf83f503cf', -1);
  INSERT INTO users (email_id, password, status) VALUES ('sinadin_b190534cs@nitc.ac.in', '75eb603c432f79e9d878ce455495f8d240975b2fcf8b258b4b9725dbe18abf3e', 0);
  INSERT INTO users (email_id, password, status) VALUES ('midhunkumar_b190439cs@nitc.ac.in', '316662b5abd17ba00c0710021ceb6a108b288fa1784eee76377265518c8234d9', 0);
  INSERT INTO users (email_id, password, status) VALUES ('jefin_b190138ce@nitc.ac.in', 'cd682626b57a7b03d5099392b33b529833f5978f18f2b763740878cb300ed7fd', 0);
  INSERT INTO users (email_id, password, status) VALUES ('celestine_b190468cs@nitc.ac.in', '903dc88feefee788746a678b5f23510a70348f797aaef047c2a7f8646b39fb0f', 0);
  INSERT INTO users (email_id, password, status) VALUES ('shehzad_b190837cs@nitc.ac.in', '98b5438076606eeb58a57f6ab03872da9149bdb75e5a57a2c948f72eadc49e60', 0);
  INSERT INTO users (email_id, password, status) VALUES ('mohammedjawad_b190441cs@nitc.ac.in', '69d9b46d704306a951eb0b757debf05a0956384635a1634897a95e1c0385e390', 0);

  INSERT INTO position (position) VALUES ('General Secretary (GS)');
  INSERT INTO position (position) VALUES ('Academic Affairs Secretary (AAS)');
  INSERT INTO position (position) VALUES ('Research Affairs Secretary (RAS)');
  INSERT INTO position (position) VALUES ('Hostel Affairs Secretary (HAS)');
  INSERT INTO position (position) VALUES ('Sports Secretary (SS)');
  INSERT INTO position (position) VALUES ('Cultural Affairs Secretary (CAS)');
  INSERT INTO position (position) VALUES ('Science & Technology Affairs Secretary (TAS)');
  INSERT INTO position (position) VALUES ('Joint Secretary (JS)');
  INSERT INTO position (position) VALUES ('Chief Student Editor (SE)');
  INSERT INTO position (position) VALUES ('Alumni Affairs Secretary (ALAS)');
