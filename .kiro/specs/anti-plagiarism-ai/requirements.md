# Requirements Document

## Introduction

The Anti-Plagiarism AI system is a full-stack web application designed to monitor and analyze coding sessions in real-time to detect potential plagiarism during programming contests. The system captures user interactions with a code editor, stores session data, and provides replay functionality for review purposes. It consists of a FastAPI backend with MongoDB storage and a React frontend with Monaco editor integration.

## Requirements

### Requirement 1

**User Story:** As a contest host, I want to create and manage programming contests so that I can organize coding competitions with proper oversight.

#### Acceptance Criteria

1. WHEN a host registers THEN the system SHALL create a user account with "host" role
2. WHEN a host logs in THEN the system SHALL return a JWT token for authentication
3. WHEN a host creates a contest THEN the system SHALL store contest details including title, description, start_time, end_time, and created_by
4. WHEN a host views contests THEN the system SHALL display all contests they have created
5. IF a host is authenticated THEN the system SHALL allow access to contest management features

### Requirement 2

**User Story:** As a student participant, I want to join programming contests and have my coding session monitored so that contest integrity is maintained.

#### Acceptance Criteria

1. WHEN a student registers THEN the system SHALL create a user account with "student" role
2. WHEN a student logs in THEN the system SHALL return a JWT token for authentication
3. WHEN a student joins a contest THEN the system SHALL add them to the contest participants list
4. WHEN a student starts coding THEN the system SHALL request consent for session monitoring
5. WHEN consent is given THEN the system SHALL generate a unique session_id and begin tracking

### Requirement 3

**User Story:** As a system administrator, I want all coding interactions to be captured and stored so that sessions can be replayed for plagiarism analysis.

#### Acceptance Criteria

1. WHEN a user types in the editor THEN the system SHALL capture keystroke events with timestamps
2. WHEN a user performs editor actions THEN the system SHALL record the action type and details
3. WHEN events are captured THEN the system SHALL batch them every 4 seconds for transmission
4. WHEN events are sent to backend THEN the system SHALL store them in the sessions collection
5. IF network fails THEN the system SHALL queue events locally until connection is restored

### Requirement 4

**User Story:** As a contest host, I want to replay participant coding sessions so that I can review their work for potential plagiarism.

#### Acceptance Criteria

1. WHEN a host requests session replay THEN the system SHALL retrieve all events for that session_id
2. WHEN events are loaded THEN the system SHALL display them in chronological order
3. WHEN replay is started THEN the system SHALL recreate the coding session step by step
4. WHEN replay is paused THEN the system SHALL maintain current state for resume
5. IF session data is corrupted THEN the system SHALL display an appropriate error message

### Requirement 5

**User Story:** As a developer, I want the system to have proper authentication and authorization so that only authorized users can access appropriate features.

#### Acceptance Criteria

1. WHEN a user registers THEN the system SHALL hash their password before storage
2. WHEN a user logs in with valid credentials THEN the system SHALL return a JWT token
3. WHEN API requests are made THEN the system SHALL validate JWT tokens
4. WHEN tokens expire THEN the system SHALL require re-authentication
5. IF invalid credentials are provided THEN the system SHALL return appropriate error messages

### Requirement 6

**User Story:** As a system operator, I want the application to be containerized and easily deployable so that setup and maintenance are simplified.

#### Acceptance Criteria

1. WHEN docker-compose is run THEN the system SHALL start all required services (backend, frontend, MongoDB)
2. WHEN backend starts THEN it SHALL listen on port 9000 with CORS enabled for localhost:5000
3. WHEN frontend starts THEN it SHALL serve on port 5000 and connect to backend API
4. WHEN MongoDB starts THEN it SHALL be accessible to the backend for data operations
5. IF any service fails THEN the system SHALL provide clear error messages and logs

### Requirement 7

**User Story:** As a developer, I want the frontend to have a modern, responsive interface so that users have a good experience across devices.

#### Acceptance Criteria

1. WHEN pages load THEN the system SHALL display responsive layouts using Tailwind CSS
2. WHEN users navigate THEN the system SHALL provide clear routing between pages
3. WHEN forms are submitted THEN the system SHALL provide immediate feedback
4. WHEN errors occur THEN the system SHALL display user-friendly error messages
5. IF the Monaco editor loads THEN it SHALL provide syntax highlighting and code completion

### Requirement 8

**User Story:** As a future developer, I want the system to have extensible architecture so that AI-based plagiarism detection can be added later.

#### Acceptance Criteria

1. WHEN session data is stored THEN it SHALL be in a format suitable for AI analysis
2. WHEN the system is designed THEN it SHALL include placeholder endpoints for feature extraction
3. WHEN new analysis features are added THEN they SHALL integrate seamlessly with existing data
4. WHEN API responses are structured THEN they SHALL support future enhancement without breaking changes
5. IF analysis modules are added THEN the system SHALL maintain backward compatibility