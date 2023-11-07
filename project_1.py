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


class CandidatesSearch:
    """
    A class for processing candidate search condition and structuring results
    """
    def __init__(self, input_conditions: List) -> None:
        self.database = DatabaseManager('mysql')
        self.candidate_data = self.database.read_data('p1_candidates')
        self.input_conditions = input_conditions

    def gender(self, gender: str = "All"):

        """
        Filters candidates by gender.

        Parameters:
        - gender (str): The gender to filter by. Should be 'M', 'F', or 'All' for all genders.

        Returns:
        List: List of candidate IDs matching the specified gender.
        """

        valid_genders = {"M", "F", "All"}
        if gender not in valid_genders:
            raise ValueError("Invalid gender argument. Please provide 'M', 'F', or 'All'.")

        if gender == "All":
            return [candidate[1] for candidate in self.candidate_data]

        return [candidate[1] for candidate in self.candidate_data if candidate[3] == gender]

    def age(self, younger_then: str = "", older_then: str = ""):

        """
        Filters candidates by age range.

        Parameters:
        - younger_then (str): The maximum age for candidates.
        - older_then (str): The minimum age for candidates.

        Returns:
        List: List of candidate IDs within the specified age range.
        """
                
        younger_then = int(younger_then) if younger_then != "" else ""
        older_then = int(older_then) if older_then != "" else ""
        current_year = datetime.date.today().year

        if younger_then != "" and older_then != "":
            return [candidate[1] for candidate in self.candidate_data if current_year - candidate[4] < younger_then and current_year - candidate[4] > older_then]
        elif younger_then != "":
            return [candidate[1] for candidate in self.candidate_data if current_year - candidate[4] < younger_then]
        elif older_then != "":
            return [candidate[1] for candidate in self.candidate_data if current_year - candidate[4] > older_then]
        else:
            return [candidate[1] for candidate in self.candidate_data]

    def condition_search(self, input, full_str: bool, data_index):
        """
        Searches for candidates based on various conditions.

        Parameters:
        - input: The search condition.
        - full_str (bool): If True, perform a full string search; if False, perform a partial string search.
        - data_index: The index of the candidate data attribute to search in.

        Returns:
        List: List of candidate IDs matching the search condition.
        """
        input_str = str(input).lower()
        if full_str:
            return [data[1] for data in self.candidate_data if str(data[data_index]).lower() == input_str]
        else:
            return [data[1] for data in self.candidate_data if input_str in str(data[data_index]).lower()]

    def merge_search_results(self):
        """
        Merges the results of various search conditions.

        Returns:
        List: List of search results for each condition.
        """
        raw_results = [
            self.gender(self.input_conditions[0]),  # gender
            self.age(younger_then=self.input_conditions[1], older_then=self.input_conditions[2]),  # age
            self.condition_search(self.input_conditions[3], False, 5),  # city
            self.condition_search(
                self.input_conditions[4], False, 11),  # education major
            self.condition_search(
                self.input_conditions[5], False, 16),  # work experience
            self.condition_search(
                self.input_conditions[6], False, 12),  # business skills
            self.condition_search(
                self.input_conditions[7], False, 13),  # licences
            self.condition_search(
                self.input_conditions[8], False, 14),  # languages
            self.condition_search(
                self.input_conditions[9], False, 17),  # optimal_position
            self.condition_search(
                self.input_conditions[10], False, 18),  # talent score
            self.condition_search(
                self.input_conditions[11], False, 20)  # blacklisted
        ]
        return raw_results

    def find_common_elements(self):
        """
        Finds common elements among multiple search results.

        Returns:
        List: List of candidate IDs that meet all search conditions.
        """
        full_list = self.merge_search_results()

        result = set(full_list[0])
        for i in range(1, len(full_list)):
            result = result & set(full_list[i])

        return list(result)

    def search_results(self):
        """
        Retrieves candidate names based on candidate ID and returns the final search list.

        Returns:
        List: Nested list of candidate IDs and their names [['0003', 'Jakemiv Ivana'], ...]
        """
        candidates_id_list = self.find_common_elements()
        data = self.candidate_data
        result = []

        for candidate_id in data:
            for result_candidate_id in candidates_id_list:
                if result_candidate_id == candidate_id[1]:
                    result.append([result_candidate_id, candidate_id[2]])

        return result


class CMSManager:
    """
    A class that manages candidate CMS operations for a specific project.

    Parameters:
    - project_id (str): The ID of the project in the CMS.

    Usage:
    ```
    manager = CMSManager(project_id)
    project_name = manager.get_project_name()
    print(f"Managing CMS for project: {project_name}")
    ```
    """
    def __init__(self, project_id: str) -> None:
        self.database = DatabaseManager('mysql')
        self.cms_data = self.database.read_data('p1_cms')
        self.candidate_data = self.database.read_data('p1_candidates')
        self.project_data = self.database.read_data('p1_projects')
        self.project_id = project_id

    def get_project_name(self):

        """
        Retrieves the name of the project associated with the specified project ID.

        Returns:
        str: The name of the project.
        """

        project_name = [name[3] for name in self.project_data if name[1] == self.project_id]
        return project_name

    def add_candidates_to_project(self):
        """
        Searches and updates the CMS database with candidates who are part of the project, not added to the project before, and not blacklisted.

        Returns:
        str: A message indicating the candidates added to the CMS database.
        """
        candidates = [candidate[1] for candidate in self.candidate_data if candidate[19]
                      == self.project_id and candidate[20] == 'False']
        candidates_not_added = [candidate for candidate in candidates if (
            self.project_id, candidate) not in [(data[1], data[2]) for data in self.cms_data]]

        sql_query = "INSERT INTO p1_cms (project_id, candidate_id) VALUES (%s, %s)"

        for candidate in candidates_not_added:
            data = (self.project_id, candidate)
            DatabaseManager(self.database).save_data(sql_query, data)

        return f"candidates with id {candidates_not_added} added to cms database"

    def get_project_data(self):
        """
        Returns a list of candidate data for the chosen project.

        Returns:
        List: List of candidate data for the specified project.
        """
        self.add_candidates_to_project()

        result = []

        for candidate_data in self.cms_data:
            if candidate_data[1] == self.project_id:
                for candidate in self.candidate_data:
                    if candidate[1] == candidate_data[2]:
                        candidate_data_list = list(candidate_data)[2:]
                        candidate_data_list.insert(1, candidate[2])
                        candidate_data_list.append('◇' if candidate[26] else '') # if candidate is interviewed
                        candidate_data_list.append(candidate_data_list[2])
                        candidate_data_list.pop(2)
                        result.append(candidate_data_list)

        result = [[item if item is not None else "" for idx, item in enumerate(sublist)] for sublist in result]
        result = [[item if idx != 7 or not item else '◈' for idx, item in enumerate(sublist)] for sublist in result] 

        return result

    def get_candidate_note(self, candidate_id: str):
        """
        Retrieves the CMS note for the selected candidate ID.

        Parameters:
        - candidate_id (str): The ID of the candidate.

        Returns:
        str: The CMS note for the candidate.
        """
        for data in self.cms_data:
            if data[1] == self.project_id and data[2] == candidate_id:
                return data[3]

    def update_candidate_note(self, candidate_id: str, note: str):
        """
        Updates the CMS note for the selected candidate ID.

        Parameters:
        - candidate_id (str): The ID of the candidate.
        - note (str): The new CMS note to be set for the candidate.

        Returns:
        str: A message indicating that the note content has been changed.
        """
        sql_query = "UPDATE p1_cms SET note = %s WHERE project_id = %s AND candidate_id = %s"
        data = (note, self.project_id, candidate_id)
        DatabaseManager(self.database).save_data(sql_query, data)

        return "Note content changed"

    def update_selection_status(self, candidate_id: str, status):
        """
        Updates the CMS selection status for the selected candidate ID.

        Parameters:
        - candidate_id (str): The ID of the candidate.
        - status (tuple): A tuple representing the new selection status.

        Returns:
        str: A message indicating that the candidate's selection status has been changed.
        """
        sql_query = "UPDATE p1_cms SET status_accepted = %s, status_reserve = %s, status_rejected = %s WHERE project_id = %s AND candidate_id = %s"
        data = (status[0], status[1], status[2], self.project_id, candidate_id)
        DatabaseManager(self.database).save_data(sql_query, data)

        return f"Candidate selection status has changed"

    def update_candidate_rating(self, candidate_id: str, score: int):
        """
        Updates the CMS candidate rating status for the selected candidate ID.

        Parameters:
        - candidate_id (str): The ID of the candidate.
        - score (int): The new rating score to be set for the candidate.

        Returns:
        str: A message indicating that the score for the candidate has been changed.
        """
        sql_query = "UPDATE p1_cms SET score = %s WHERE project_id = %s AND candidate_id = %s"
        data = (score, self.project_id, candidate_id)
        DatabaseManager(self.database).save_data(sql_query, data)

        return f"Score for candidate_id: {candidate_id} has changed to: {score}"

    def select_update(self, input_data):
        """
        Calls status or score update depending on the size of the input.

        Parameters:
        - input_data (List): A list of data for updating status or score.

        Returns:
        str: A message indicating the success of the status or score update.
        """
        if len(input_data) == 3:
            self.update_candidate_rating(input_data[1], input_data[2])
            return "Candidate score successfully updated"
        elif len(input_data) == 5:
            status = input_data[2:]
            self.update_selection_status(input_data[1], status)
            return "Candidate status successfully updated"
