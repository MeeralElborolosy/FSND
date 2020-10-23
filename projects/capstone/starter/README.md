# Mentorship Application
# Description:
This API manages a mentorship program. Participants in this program may either be mentors or mentees. Participants may
enroll in one or more projects. There are no restrictions to the number of mentors or mentees per project. An admin has
an almost unlimited access to the API except that they can't rate participants. Users may rate participants,
view participants and projects as well as search for a project by description.
# Models:
* Participant:

    A participant has a name, skills, and a boolean attribute that determines whether or not they're a mentor
* Project:

    A project has a name, a description, a start date set once it's created and an end date set when its corresponding endpoint is called
* Participant_Project Relationship:

    Participants and projects have a many to many relationship. One participant can be enrolled in multiple projects and a single project may have multiple enrolled partiicpants
# Roles:
* Admin:

    Can access all endpoints except PATCH r'/participants/\<int:id>/rate'
* User:

    Can only access the GET endpoints, POST '/projects/search?page=<page_number>' and PATCH r'/participants/\<int:id>/rate'
# Endpoints:
* GET '/mentors?page=<page_number>'
- Fetches paginated mentors with the limit of 10 mentors per page
- Request arguments: page number(default=1)
- Possible errors: 404 resource not found
- Returns: mentors(formatted mentors) and total_mentors(total number of mentors).
* GET '/mentees?page=<page_number>'
- Fetches paginated mentees with the limit of 10 mentees per page
- Request arguments: page number(default=1)
- Possible errors: 404 resource not found
- Returns: mentees(formatted mentees) and total_mentees(total number of mentees).
* GET '/participants?page=<page_number>'
- Fetches paginated participants with the limit of 10 participants per page
- Request arguments: page number(default=1)
- Possible errors: 404 resource not found
- Returns: participants(formatted participants) and total_participants(total number of participants).
* GET '/projects?page=<page_number>'
- Fetches paginated projects with the limit of 10 projects per page
- Request arguments: page number(default=1)
- Possible errors: 404 resource not found
- Returns: projects(formatted projects) and total_projects(total number of projects).
* GET r'/participants/<int:id\>'
- Fetches participant by id
- Request arguments: None
- Possible errors: 404 resource not found
- Returns: participant(formatted participant)
* GET r'/participants/<int:id\>/projects'
- Fetches projects that a certain participant is enrolled in
- Possible errors: 404 resource not found
- Returns: a list of projects ids(projects)
* GET r'/projects/<int:id\>'
- Fetches project by id
- Request arguments: None
- Possible errors: 404 resource not found
- Returns: formatted participant(participant)
* GET r'/projects/<int:id\>/participants'
- Fetches particpants that are enrolled in a certain project
- Request arguments: None
- Possible errors: 404 resource not found
- Returns: a list of participants ids(participants)
* POST '/projects/search?page=<page_number>' json = {'search_term': \< string: SEARCH_TERM > }
- Fetches pagenated projects that include a certain search term
- Request arguments: page number(default=1)
- Possible errors: 422 unprocessable or 404 resource not found
- Returns: pagenated projects that contain the search term(projects) and total number of projects(total_projects)
* POST '/participants?page=<page_number>' json = {'name': \< string: NAME > , 'skills': \< string: SKILLS > , 'is_mentor': \< bool: IS_MENTOR > }
- Creates a new participant
- Request arguments: page number(default=1)
- Possible errors: 422 unprocessable
- Returns: new participant id(created), formatted pagenated participants(participants) and total number of participants(total_participants)
* POST '/projects' json = {'name': \< string: NAME > , 'description': \< string: DESCRIPTION > }
- Creates a new project
- Request arguments: page number(default=1)
- Possible errors: 422 unprocessable
- Returns: new project id(created), formatted pagenated projects(projects) and total number of projects(total_projects)
* PATCH r'/projects/<int:id\>'
- Sets project end_date to current datetime
- Request arguments: None
- Possible errors: 404 resource not found
- Returns: formatted project(project)
* PATCH '/participants/\<int:id>/rate' json = {'rating': \< int: RATING > }
- Changes participant rating to the average of previous ratings and the new one
- Request arguments: None
- Possible errors: 422 unprocessable or 404 resource not found
- Returns formatted participant(participant)
* PATCH r'participants/<int:participant_id\>/enroll/<int:project_id\>'
- Enrolls a certain participant in a certain project
- Request arguments: None
- Possible errors: 422 unprocessable or 404 resource not found
- Returns: formatted participant(participant)
* DELETE r'participants/<int:id\>'
- Deletes a certain participant
- Request arguments: None
- Possible errors: 404 resource not found
- Returns: deleted participant id(deleted)
* DELETE r'projects/<int:id\>'
- Deletes a certain project
- Request arguemnts: None
- Possible errors: 404 resource not found
- Returns: deletes project id(deleted)
