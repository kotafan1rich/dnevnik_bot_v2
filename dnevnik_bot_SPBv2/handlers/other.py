import aiohttp

from config import API_URL


async def user_exists(id_tg):
	"""
	Проверяет, существует ли пользователь по его Telegram ID.

	Эта асинхронная функция отправляет запрос к внешнему API, чтобы определить, существует ли пользователь с указанным Telegram ID. Она возвращает булево значение, указывающее на существование пользователя.

	Args:
	        id_tg (str): Telegram ID пользователя для проверки.

	Returns:
	        bool: True, если пользователь существует, иначе False.
	"""

	async with aiohttp.ClientSession() as session:
		params = {"tg_id": id_tg}
		async with session.get(f"{API_URL}/user/by_id_tg", params=params) as response:
			return response.status == 200


async def add_user(id_tg):
	"""
	Добавляет пользователя по его Telegram ID.

	Эта асинхронная функция отправляет запрос на добавление пользователя в систему, используя указанный Telegram ID. Она возвращает статус ответа от API, который указывает на результат операции.

	Args:
	        id_tg (str): Telegram ID пользователя, которого необходимо добавить.

	Returns:
	        int: Статус ответа от API, указывающий на результат операции.
	"""

	async with aiohttp.ClientSession() as session:
		params = {"id_tg": str(id_tg)}
		async with session.post(f"{API_URL}/user", params=params) as response:
			return response.status


async def get_user_info(id_tg) -> dict:
	"""
	Получает информацию о пользователе по его Telegram ID.

	Эта асинхронная функция запрашивает информацию о пользователе из внешнего API. Если пользователь не найден, функция добавляет его и повторно запрашивает информацию, возвращая данные в виде словаря.

	Args:
	        id_tg (str): Telegram ID пользователя, информацию о котором необходимо получить.

	Returns:
	        dict: Информация о пользователе, полученная из API.
	"""

	async with aiohttp.ClientSession() as session:
		params = {"tg_id": id_tg}
		async with session.get(f"{API_URL}/user/by_id_tg", params=params) as response:
			if response.status == 404:
				add_user_response = await add_user(id_tg)
				if add_user_response:
					async with session.get(
						f"{API_URL}/user/by_id_tg", params=params
					) as response_final:
						return await response_final.json()
			return await response.json()


def get_clean_user_info(user_info):
	"""
	Форматирует и очищает информацию о пользователе для удобного отображения.

	Эта функция принимает словарь с информацией о пользователе и возвращает строку, содержащую отформатированные данные о группе, образовании и JWT-токене. Если токен отсутствует, в строке будет указано "None".

	Args:
	        user_info (dict): Словарь с информацией о пользователе, содержащий ключи "group_id", "education_id" и "jwt_token".

	Returns:
	        str: Отформатированная строка с информацией о пользователе.
	"""

	group_id: str = f'group_id: {user_info.get("group_id")}'
	education_id: str = f'education_id: {user_info.get("education_id")}'
	jwt_token: str = (
		f'jwt_token: {"добавлен" if bool(user_info.get("jwt_token")) else "None"}'
	)
	return "\n".join((education_id, group_id, jwt_token))


async def save_user_info(id_tg: int, user_info: dict):
	"""
	Сохраняет информацию о пользователе по его Telegram ID.

	Эта асинхронная функция отправляет запрос на обновление информации о пользователе в систему, используя указанный Telegram ID и данные пользователя. Она возвращает статус ответа от API, который указывает на результат операции.

	Args:
	        id_tg (int): Telegram ID пользователя, информацию о котором необходимо сохранить.
	        user_info (dict): Словарь с информацией о пользователе для обновления.

	Returns:
	        int: Статус ответа от API, указывающий на результат операции.
	"""

	async with aiohttp.ClientSession() as session:
		params = {"id_tg": id_tg}
		async with session.post(
			f"{API_URL}/user/update", params=params, json=user_info
		) as response:
			return response.status


def _abbreviation(marks_res: str):
	"""
	Заменяет полные названия предметов на их сокращения.

	Эта функция принимает строку с названиями предметов и возвращает её, заменяя определённые полные названия на общепринятые аббревиатуры. Это упрощает представление информации о предметах.

	Args:
	        marks_res (str): Строка с полными названиями предметов.

	Returns:
	        str: Строка с заменёнными аббревиатурами предметов.
	"""

	return (
		marks_res.replace("Основы безопасности и защиты Родины", "ОБЗР")
		.replace("Изобразительное искусство", "ИЗО")
		.replace("Физическая культура", "Физ-ра")
		.replace("Иностранный язык (английский)", "Английский язык")
		.replace("История России. Всеобщая история", "История")
		.replace("Иностранный язык (английский язык)", "Английский язык")
		.replace("Алгебра и начала математического анализа", "Алгебра")
		.replace("Вероятность и статистика", "Вер. и статистика")
	)


def _sort_quater(subject_data, subject) -> str:
	"""
	Форматирует и сортирует данные о предмете для отображения.

	Эта функция принимает данные о предмете и возвращает строку, содержащую отформатированную информацию, включая последние оценки, среднюю оценку и целевую оценку. Она помогает представить информацию о предмете в удобочитаемом виде.

	Args:
	        subject_data (dict): Словарь с данными о предмете, включая оценки и целевую оценку.
	        subject (str): Название предмета.

	Returns:
	        str: Отформатированная строка с информацией о предмете.
	"""

	average = subject_data.get("average", [None])[0]
	count = subject_data.get("count_marks", [None])[0]
	target_grade = subject_data["target_grade"] or ""
	final_m = ""
	if subject_data["final_q"]:
		final_m = "=> " + str(subject_data["final_q"][0])
	last_3 = " ".join(list(map(str, subject_data["last_three"])))
	return f"<i>{subject}</i>  {last_3}  ({count})  <i>{average}</i> {final_m} {target_grade}\n"


def _sort_year(sub_data: dict, subject) -> str:
	"""
	Форматирует и сортирует данные о предмете за год для отображения.

	Эта функция принимает данные о предмете за год и возвращает строку, содержащую отформатированную информацию, включая среднюю оценку, количество оценок и финальные результаты. Она помогает представить информацию о предмете в удобочитаемом виде.

	Args:
	        sub_data (dict): Словарь с данными о предмете, включая финальные оценки и среднюю оценку.
	        subject (str): Название предмета.

	Returns:
	        str: Отформатированная строка с информацией о предмете за год.
	"""

	finals_q = " ".join(map(str, sub_data["final_q"][::-1]))
	finals_y = (
		"=> " + str(sub_data["final_years"][0]) if sub_data["final_years"] else ""
	)
	final = "| " + str(sub_data["final"][0]) if sub_data["final"] else ""
	return f"<i>{subject}</i>  {sub_data['average'][0]} ({sub_data['count_marks'][0]}) {finals_q} {finals_y} {final}\n"


def sort_marks(data: dict, period_name) -> str:
	"""
	Сортирует и форматирует оценки за указанный период.

	Эта функция принимает данные об оценках и возвращает строку, содержащую отформатированную информацию о предметах, включая средние баллы за аттестацию. Она позволяет удобно представить оценки за год или четверть в зависимости от указанного периода.

	Args:
	        data (dict): Словарь с данными об оценках, включая средние баллы и информацию по предметам.
	        period_name (str): Название периода, за который необходимо отобразить оценки (например, "Год" или "Четверть").

	Returns:
	        str: Отформатированная строка с оценками и средними баллами.
	"""

	result = f"{period_name}\n\n"

	finals_average = data["finals_average_q"]
	all_finals_y = data["finals_average_y"]

	for subject, subject_data in data.get("marks_data").items():
		if subject not in ["finals_average_q", "finals_average_y"]:
			if period_name == "Год":
				result += _sort_year(subject_data, subject)
			else:
				result += _sort_quater(subject_data, subject)
	if finals_average:
		result += f"\nСр. балл аттестации - {finals_average}"
	if all_finals_y:
		result += f"\nСр. балл итоговой аттестации - {all_finals_y}"
	return _abbreviation(result)


async def get_marks(id_tg: int, period: str):
	"""
	Получает оценки пользователя за указанный период.

	Эта асинхронная функция запрашивает оценки пользователя по его Telegram ID и заданному периоду, а затем возвращает отформатированную строку с оценками. Если оценки отсутствуют, функция сообщает об этом, а в случае ошибки возвращает сообщение об ошибке.

	Args:
	        id_tg (int): Telegram ID пользователя, чьи оценки необходимо получить.
	        period (str): Название периода, за который нужно получить оценки.

	Returns:
	        str: Отформатированная строка с оценками или сообщение об отсутствии оценок или ошибке.
	"""

	async with aiohttp.ClientSession() as session:
		params = {"id_tg": id_tg}
		async with session.get(
			f"{API_URL}/marks/get_user_periods", params=params
		) as response_period:
			data: dict = await response_period.json()
			period_data: dict = data.get("result").get(period)
			period_id, date_from, date_to = (
				period_data["id"],
				period_data["date_from"],
				period_data["date_to"],
			)
			params = {
				"id_tg": id_tg,
				"date_from": date_from,
				"date_to": date_to,
				"period_id": period_id,
			}
			async with session.get(f"{API_URL}/marks", params=params) as response_marks:
				if response_marks and response_marks.status == 200:
					json = await response_marks.json()
					marks = json.get("result")
					if marks.get("marks_data"):
						return sort_marks(marks, period)
					return f"Нет оценок за {period}"
				else:
					return "Ошибка..."
