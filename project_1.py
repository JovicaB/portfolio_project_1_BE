import datetime
from data.database import DatabaseManager
from typing import List


class Dashboard:
    """
    A class for structuring and analyzing data related to clients, projects, and candidates.

    Attributes:
        work_experience_levels (list): A list of work experience levels.
        work_experience_no_levels (list): A list of work experience without levels.

    Methods:
        _client_stat(): Counts the number of clients.
        _projects_stat(): Counts the number of projects.
        _candidates_basic_stat(): Counts basic statistics for candidates.
        _candidates_work_experience_counter(work_experience_input_list): Counts work experience occurrences based on a list.
        statistics(): Merges statistics data for clients, projects, and candidates.

    Usage:
    ```
    dashboard_data = Dashboard().statistics()
    ```
    """
    work_experience_levels = ['MNG-E', 'MNG-M', 'MNG-S', 'CON-E', 'CON-M', 'CON-S', 'COM-E', 'COM-M', 'COM-S', 'RET-E', 'RET-M', 'RET-S', 'MAR-E',
                              'MAR-M', 'MAR-S', 'BAN-E', 'BAN-M', 'BAN-S', 'ACC-E', 'ACC-M', 'ACC-S', 'PRD-E', 'PRD-M', 'PRD-S', 'CUL-E', 'CUL-M', 'CUL-S', 'HR-E', 'HR-M', 'HR-S']
    work_experience_no_levels = ['ADM', 'COP', 'DIS', 'WHW', 'DES', 'DSK',
                                 'FIN', 'MNL', 'HOT', 'WTR', 'LOG', 'NUR', 'PUB', 'MNT', 'BSA', 'PRM']

    def __init__(self) -> None:
        self.database = DatabaseManager('mysql')
        self.client_data = self.database.read_data('p1_clients')
        self.projects_data = self.database.read_data('p1_projects')
        self.candidates_data = self.database.read_data('p1_candidates')
        self.statistics_data = []

    def _client_stat(self):
        """
        Counts the number of clients.

        Returns:
        int: The number of clients.
        """
        result = len(self.client_data) if self.client_data else 0
        return result

    def _projects_stat(self):
        """
        Counts the number of projects.

        Returns:
        int: The number of projects.
        """
        result = len(self.projects_data) if self.projects_data else 0
        return result

    def _candidates_basic_stat(self):
        """
        Counts basic statistics about candidates.

        Returns:
        list: A list of 5 values representing various statistics.
        """
        count_candidates = len(self.candidates_data)
        count_candidates_interviewed = sum(
            1 for item in self.candidates_data if item[26] != "")
        count_candidates_knowledge_tested = sum(
            1 for item in self.candidates_data if item[21] is not None or item[23] is not None)
        count_candidates_talent_scored = sum(
            1 for item in self.candidates_data if item[18] != "" and item[18] > 0)
        count_candidates_blacklisted = sum(
            1 for item in self.candidates_data if item[20] == 'True')

        result = [
            count_candidates,
            count_candidates_interviewed,
            count_candidates_knowledge_tested,
            count_candidates_talent_scored,
            count_candidates_blacklisted
        ]
        return result

    def _candidates_work_experience_counter(self, work_experience_input_list):
        """
        Counts work experience occurrences based on a list.

        Parameters:
        work_experience_input_list (list): A list of work experience to count.

        Returns:
        list: A list of counts for each work experience item.
        """
        work_experience_data_list = [we[16] for we in self.candidates_data]
        occurrences_counter_list = []

        for we in work_experience_input_list:
            count = sum(
                1 for item in work_experience_data_list if we in item.split(':'))
            occurrences_counter_list.append(count)

        return occurrences_counter_list

    def statistics(self):
        """
        Merges statistics data for clients, projects, and candidates.

        Returns:
        dict: A dictionary with statistics for clients, projects, and candidates.
        """
        result = {
            'clients': self._client_stat(),
            'projects': self._projects_stat(),
            'candidates_basic': self._candidates_basic_stat(),
            'candidates_we_levels': self._candidates_work_experience_counter(self.work_experience_levels),
            'candidates_we_no_levels': self._candidates_work_experience_counter(self.work_experience_no_levels)
        }

        return result


class Clients:
    """
    A class for managing client data (preview, insert, and data update).
    """
    def __init__(self) -> None:
        self.database = DatabaseManager('mysql')
        self.client_data = self.database.read_data('p1_clients')


    def preview_clients(self):
        """
        Retrieves a preview of client data as a nested list.

        Returns:
        List: A nested list of client data, where each inner list consists of [client_id, client_name].
        """
        result = [[val[1], val[2]] for val in self.client_data]
        return result

    def get_edit_client_data(self, client_id):
        """
        Retrieves and displays client data based on the provided client_id.

        Parameters:
            client_id (str): The unique identifier of the client.

        Returns:
        List: A list of client data, including company, city, industry, note, contact name, phone, and email.
        """
        result = [val[1:]
                  for val in self.client_data if val[1] == client_id][0]
        return result

    def add_edit_client(self, data: List):
        """
        Adds a new client or edits an existing client's data based on the provided information.

        Parameters:
            data (List): A list of client data to be added or edited. The first element of the list should be a boolean value (True for adding, False for editing), followed by company, city, industry, note, contact name, phone, and email.

        Returns (str): A message indicating whether the client was added or its data was edited.
        """
        condition = data[0]
        data = data[1:]
        if condition == 'True':
            data.insert(0, self.generate_client_id())
            data = tuple(data)
            self.add_client(data)
            return f"client with id {data[0]} added to database"
        else:
            data = tuple(data[1:]) + (data[0],)
            self.edit_client(data)
            return f"client data with id {data[-1]} edited"

    def generate_client_id(self):
        """
        Generates a new client ID for adding a client.

        Returns (str): A newly generated client ID.
        """
        data = [int(x[1]) for x in self.client_data]
        max_id = max(data) + 1 if data else 1
        new_client_id = f"{max_id:04d}"
        return new_client_id

    def add_client(self, data: List):
        """
        Adds a new client to the database.

        Parameters:
            data (List): A list of client data to be added, including client_id, company, city, industry, note, contact name, phone, and email.

        Returns (str): A message confirming that the client has been added to the database.
        """
        sql_query = "INSERT INTO p1_clients (client_id, company, city, industry, note, ci_name, ci_phone, ci_email) " \
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s)"
        self.database.save_data(sql_query, data)
        return f"client with id {data[0]} added to database"

    def edit_client(self, data: List):
        """
        Edits an existing client's data in the database.

        Parameters:
            data (List): A list of client data to be edited, including company, city, industry, note, contact name, phone, email, and client_id.

        Returns (str): A message confirming that the client's data has been edited.
        """
        sql_query = "UPDATE p1_clients SET company = %s, city = %s, industry = %s, note = %s, ci_name = %s, ci_phone = %s, ci_email = %s WHERE client_id = %s"
        self.database.save_data(sql_query, data)
        return f"client data with id {data[0]} edited"
    

class Projects:
    """
    A class for managing project data (preview, insert and data update)
    """
    def __init__(self) -> None:
        self.database = DatabaseManager('mysql')
        self.projects_data = self.database.read_data('p1_projects')

    def preview_projects(self):
        """
        Retrieves a preview of projects data as a nested list.

        Returns:
        List: A nested list of project data, where each inner list consists of [project, client_id, job_position].
        """
        result = [[val[1], val[2], val[3]] for val in self.projects_data]
        return result

    def get_edit_project_data(self, project_id):
        """
        Retrieves and displays project data based on the provided project_id.

        Parameters:
            project_id (str): The unique identifier of the project.

        Returns:
        List: A list of project data, including client_id, job_title, job_description, ...
        """
        result = [val[1:]
                  for val in self.projects_data if val[1] == project_id][0]
        return result

    def add_edit_project(self, data: List):
        """
        Adds a new project or edits an existing project's data based on the provided information.

        Parameters:
            data (List): A list of project data to be added or edited. The first element of the list should be a boolean value (True for adding, False for editing), followed by client_id, ...

        Returns (str): A message indicating whether the client was added or its data was edited.
        """
        condition = data[0]
        data = data[1:]
        if condition == 'True':
            data.insert(0, self.generate_project_id())
            data = tuple(data)
            self.add_project(data)
            return f"project with id {data[0]} added to the database"
        else:
            data = tuple(data[1:]) + (data[0],)
            self.edit_project(data)
            return f"project data with id {data[-1]} edited"

    def generate_project_id(self):
        """
        Generates a new project ID for adding a project.

        Returns (str): A newly generated project ID.
        """
        data = [int(x[1]) for x in self.projects_data]
        max_id = max(data) + 1 if data else 1
        new_project_id = f"{max_id:04d}"
        return new_project_id

    def add_project(self, data: List):
        """
        Adds a new project to the database.

        Parameters:
            data (List): A list of project data to be added, including project_id, client_id,...

        Returns (str): A message confirming that the project has been added to the database.
        """
        sql_query = "INSERT INTO p1_projects (project_id, client, project_name, job_position, number_employees, note, compensation) VALUES (%s, %s, %s, %s, %s, %s, %s)"
        DatabaseManager(self.database).save_data(sql_query, data)
        return f"project with id {data[0]} added to the database"

    def edit_project(self, data: List):
        """
        Edits an existing project's data in the database.

        Parameters:
            # data (List): A list of project data to be edited...

        Returns (str): A message confirming that the project's data has been edited.
        """
        sql_query = "UPDATE p1_projects SET client = %s, project_name = %s, job_position = %s, number_employees = %s, note = %s, compensation = %s WHERE project_id = %s"
        DatabaseManager(self.database).save_data(sql_query, data)
        return f"project data with id {data[0]} edited"


class Candidates:
    """
    A class for managing the creation and update of candidate dossiers.

    Attributes:
    - database (DatabaseManager): A database manager instance.
    - candidate_data (List): List of candidate data retrieved from the database.

    Methods:
    - get_edit_candidate_data(candidate_id: str) -> List: Returns candidate data based on the candidate ID.
    - add_edit_candidate(data: List) -> str: Selects either the 'add_candidate' or 'edit_candidate' method based on data[0] boolean value.
    - generate_candidate_id() -> str: Generates a new candidate ID.
    - add_candidate(data: List) -> str: Adds a new candidate dossier to the database.
    - edit_candidate(data: List) -> str: Edits candidate dossier data in the database.

    Usage:
    ```
    candidates = Candidates()
    
    # Retrieve candidate data for editing
    candidate_data = candidates.get_edit_candidate_data('candidate_id')
    print(candidate_data)

    # Add or edit a candidate entry
    data = [True, ...]  # True for editing, False for adding
    result = candidates.add_edit_candidate(data)
    print(result)
    ```
    """

    def __init__(self) -> None:
        self.database = DatabaseManager('mysql')
        self.candidate_data = self.database.read_data('p1_candidates')

    def get_edit_candidate_data(self, candidate_id):
        """
        Returns candidate data based on the candidate ID.

        Parameters:
        - candidate_id (str): Candidate's ID.

        Returns:
        List: Candidate data.
        """

        result = [val[1:]
                  for val in self.candidate_data if val[1] == candidate_id][0]
        return result

    def add_edit_candidate(self, data: List):
        """
        Selects 'add_candidate' or 'edit_candidate' method based on data[0] boolean value.

        Parameters:
        - data (List): List of candidate data. The first element should be a boolean indicating whether to add or edit.

        Returns:
        str: A confirmation message.
        """

        condition = data[0]
        candidate_data = data[1:]

        if condition is False:
            candidate_data.insert(0, self.generate_candidate_id())
            candidate_data = tuple(candidate_data)
            self.add_candidate(candidate_data)
            return f"candidate with id {candidate_data[0]} added to database"
        else:
            candidate_data = tuple(candidate_data[1:]) + (candidate_data[0],)
            self.edit_candidate(candidate_data)
            return f"client data with id {candidate_data[-1]} edited"

    def generate_candidate_id(self):
        """
        Generates a new candidate ID.

        Returns:
        str: New candidate ID.
        """

        data = [int(x[1]) for x in self.candidate_data]
        max_id = max(data) + 1 if data else 1
        new_candidate_id = f"{max_id:04d}"
        return new_candidate_id

    def add_candidate(self, data: List):
        """
        Adds a new candidate dossier to the database.

        Parameters:
        - data (List): List of candidate data.

        Returns:
        str: A confirmation message.
        """
        sql_query = "INSERT INTO p1_candidates (candidate_id, name_surname, gender, birth_year, city, phone, mail, linkedin, note, school, major, business_skills, licences, languages, current_position, work_experience, optimal_position, talent_score, project_ID, blacklisted, kn1_description, kn1_score, kn2_description, kn2_score, competencies, c_description, pv_description) " \
                    "VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)"

        DatabaseManager(self.database).save_data(sql_query, data)
        return f"candidate with id {data[0]} added to database"

    def edit_candidate(self, data: List):
        """
        Edits candidate dossier data in the database.

        Parameters:
        - data (List): List of candidate data to be edited.

        Returns:
        str: A confirmation message.
        """
        sql_query = "UPDATE p1_candidates SET name_surname = %s, gender = %s, birth_year = %s, city = %s, phone = %s, mail = %s, linkedin = %s, note = %s, school = %s, major = %s, business_skills = %s, licences = %s, languages = %s, current_position = %s, work_experience = %s, optimal_position = %s, talent_score = %s, project_id = %s, blacklisted = %s, kn1_description = %s, kn1_score = %s, kn2_description = %s, kn2_score = %s, competencies = %s, c_description = %s, pv_description = %s WHERE candidate_id = %s"

        DatabaseManager(self.database).save_data(sql_query, data)
        return f"client data with id {data[0]} edited"
