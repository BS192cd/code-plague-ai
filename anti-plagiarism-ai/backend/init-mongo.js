// MongoDB initialization script for Anti-Plagiarism AI

// Switch to the application database
db = db.getSiblingDB('anti_plagiarism_ai');

// Create application user
db.createUser({
  user: 'app_user',
  pwd: 'app_password123',
  roles: [
    {
      role: 'readWrite',
      db: 'anti_plagiarism_ai'
    }
  ]
});

// Create collections with validation
db.createCollection('users', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: ['username', 'password_hashed', 'role', 'created_at'],
      properties: {
        username: {
          bsonType: 'string',
          minLength: 3,
          maxLength: 50
        },
        password_hashed: {
          bsonType: 'string'
        },
        role: {
          enum: ['host', 'student']
        },
        created_at: {
          bsonType: 'date'
        },
        updated_at: {
          bsonType: 'date'
        }
      }
    }
  }
});

db.createCollection('contests', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: ['title', 'description', 'start_time', 'end_time', 'created_by', 'created_at'],
      properties: {
        title: {
          bsonType: 'string',
          minLength: 1,
          maxLength: 200
        },
        description: {
          bsonType: 'string',
          maxLength: 1000
        },
        start_time: {
          bsonType: 'date'
        },
        end_time: {
          bsonType: 'date'
        },
        created_by: {
          bsonType: 'string'
        },
        participants: {
          bsonType: 'array',
          items: {
            bsonType: 'string'
          }
        },
        status: {
          enum: ['upcoming', 'active', 'completed', 'cancelled']
        }
      }
    }
  }
});

db.createCollection('sessions', {
  validator: {
    $jsonSchema: {
      bsonType: 'object',
      required: ['session_id', 'user_id', 'language', 'created_at'],
      properties: {
        session_id: {
          bsonType: 'string'
        },
        user_id: {
          bsonType: 'string'
        },
        contest_id: {
          bsonType: 'string'
        },
        language: {
          bsonType: 'string'
        },
        events: {
          bsonType: 'array'
        },
        status: {
          enum: ['active', 'completed', 'flagged', 'suspended']
        }
      }
    }
  }
});

db.createCollection('analytics');
db.createCollection('events');
db.createCollection('ws_connections');

print('MongoDB initialization completed successfully');
print('Database: anti_plagiarism_ai');
print('Collections created: users, contests, sessions, analytics, events, ws_connections');
print('Application user created: app_user');