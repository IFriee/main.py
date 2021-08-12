--
-- Fichier g�n�r� par SQLiteStudio v3.3.3 sur lun. ao�t 9 14:05:49 2021
--
-- Encodage texte utilis� : System
--
PRAGMA foreign_keys = off;
BEGIN TRANSACTION;

-- Table : scores
CREATE TABLE scores (ID_users INTEGER REFERENCES users (ID), gains DOUBLE NOT NULL, multiplicateur DOUBLE NOT NULL);

-- Table : users
CREATE TABLE users (ID INTEGER PRIMARY KEY AUTOINCREMENT, pseudo TEXT UNIQUE, mdp TEXT NOT NULL, porte_feuilles DOUBLE NOT NULL DEFAULT (5000));
INSERT INTO users (ID, pseudo, mdp, porte_feuilles) VALUES (1, 'azerty', 'az', '');

COMMIT TRANSACTION;
PRAGMA foreign_keys = on;
