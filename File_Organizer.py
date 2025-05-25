# File Organizer v1.0 pre1
# Copyright (c) 2025 IQUXAe
# Released under the MIT License. See LICENSE file for details.

import os
import shutil
import tkinter as tk
from tkinter import filedialog, scrolledtext, messagebox, ttk, simpledialog
import threading
from datetime import datetime
import locale
import configparser
import json
import sys
import subprocess
import uuid

LANGUAGES = {
    "ru": {
        "title": "File Organizer v1.0 pre1 - Русский",
        "browse_folder_label": "Папка для сортировки:",
        "browse_button": "Обзор...",
        "open_folder_button": "Открыть папку",
        "undo_last_sort_button": "Отменить последнюю сортировку",
        "categories_label": "Категории для сортировки",
        "select_all_button": "Выбрать все",
        "deselect_all_button": "Снять все",
        "options_label": "Дополнительные опции",
        "dry_run_checkbox": "Предварительный просмотр (без перемещения файлов)",
        "organize_by_date_checkbox": "Создавать подпапки ГГГГ/ММ внутри категорий (по дате изменения)",
        "conflict_label": "При конфликте имен:",
        "conflict_rename": "Переименовать (1,2,3...)",
        "conflict_skip": "Пропустить файл",
        "start_button_idle": "Начать организацию",
        "start_button_busy": "Идет сортировка...",
        "log_label": "Лог операций:",
        "info_label_template": "File Organizer v1.0 pre1 от IQUXAe",
        "error_no_folder_selected_title": "Ошибка",
        "error_no_folder_selected_message": "Пожалуйста, выберите папку для сортировки.",
        "error_critical_title": "Критическая ошибка",
        "error_critical_message_template": "Произошла непредвиденная ошибка: {error}",
        "info_completed_title": "Завершено",
        "info_completed_message": "Организация файлов завершена!",
        "log_starting_organization": "Начинаю организацию файлов в директории: {directory}",
        "log_dry_run_active": "РЕЖИМ ПРЕДВАРИТЕЛЬНОГО ПРОСМОТРА (DRY RUN): Файлы не будут перемещены.",
        "log_date_organization_active": "Опция 'Организовать по дате (ГГГГ/ММ)' активна.",
        "log_conflict_resolution_strategy": "Стратегия разрешения конфликтов имен: {strategy}",
        "log_folder_created": "Создана папка: {folder}",
        "log_error_creating_folder": "Ошибка при создании папки {folder}: {error}",
        "log_skipping_file_exists_conflict": "Пропуск: Файл '{filename}' уже существует в '{category_path_on_disk}' и будет пропущен.",
        "log_renaming_file_conflict": "Конфликт: Файл '{original_filename}' будет переименован в '{new_filename}' в папке '{category_path_on_disk}'.",
        "log_moving_file": "{action_prefix}Перемещение: '{filename}' -> '{category_path_on_disk}/{new_filename}'",
        "log_error_moving_file": "Ошибка при перемещении файла '{filename}': {error}",
        "log_total_files_action": "Всего файлов {action}: {count}",
        "log_action_analyzed": "проанализировано",
        "log_action_moved": "обработано и перемещено",
        "log_no_new_files": "Новых файлов для анализа/перемещения не найдено или все подходящие файлы уже отсортированы.",
        "log_organization_complete": "Организация файлов завершена.",
        "log_summary_moved_to": "Перемещено в '{category_folder_name}': {count} файл(ов).",
        "log_summary_no_files_moved": "Файлы не были перемещены.",
        "log_folder_selected": "Выбрана папка: {folder}",
        "log_date_warning_template": "Предупреждение: Не удалось получить дату для файла '{filename}', не будет отсортирован по дате. Ошибка: {error}",
        "log_skipping_ignored_folder": "Пропуск игнорируемой папки: {folder_name}",
        "log_skipping_category_folder": "Пропуск папки категории: {folder_name}",
        "language_label": "Язык (Language):",
        "program_settings_label": "Настройки:",
        "settings_saved_title": "Настройки сохранены",
        "settings_saved_message": "Текущие настройки автоматически сохранены.",
        "settings_load_error_title": "Ошибка загрузки настроек",
        "settings_load_error_message": "Не удалось загрузить настройки из файла: {filepath}\nОшибка: {error}",
        "settings_file_not_found": "Файл настроек не найден: {filepath}",
        "settings_file_filter_name": "Файлы настроек",
        "warning_pre_sort_title": "Внимание перед сортировкой!",
        "warning_pre_sort_message": "Перед началом организации файлов, пожалуйста, убедитесь, что:\n1. Все файлы в выбранной папке ({folder}) закрыты во всех программах.\n2. Вы не выбрали для сортировки папку, содержащую этот или другие важные системные/программные файлы.\n\nПродолжить?",
        "error_sorting_program_folder_title": "Ошибка безопасности",
        "error_sorting_program_folder_message": "Вы пытаетесь отсортировать папку, в которой находится сама программа File Organizer, или ее родительскую папку. Это действие запрещено во избежание повреждения программы.\n\nПожалуйста, выберите другую папку.",
        "customize_categories_button": "Настроить категории...",
        "user_categories_title": "Настройка категорий",
        "user_cat_folder_name_label": "Имя папки на диске:",
        "user_cat_extensions_label": "Расширения (через запятую, напр. .aaa,.bbb):",
        "user_cat_add_button": "Добавить (пользовательскую)",
        "user_cat_edit_button": "Редактировать выбранную",
        "user_cat_update_button": "Обновить категорию",
        "user_cat_cancel_edit_button": "Отменить редактирование",
        "user_cat_remove_button": "Удалить (пользовательскую)",
        "user_cat_save_close_button": "ОК (Сохранить изменения)",
        "user_cat_list_label": "Категории сортировки (стандартные и пользовательские):",
        "user_cat_info_delete": "Примечание: Имя папки на диске и расширения можно менять для всех категорий. Пользовательские категории можно удалять.",
        "user_cat_empty_name_error_title": "Ошибка",
        "user_cat_empty_name_error_message": "Имя папки категории не может быть пустым.",
        "user_cat_empty_ext_error_message": "Список расширений не может быть пустым. Укажите хотя бы одно расширение (напр. .txt).",
        "user_cat_invalid_ext_error_message": "Расширения должны начинаться с точки (напр. .txt, .docx).",
        "user_cat_name_exists_error_message": "Категория с таким именем папки '{folder_name}' уже существует.",
        "user_cat_extension_conflict_error_message": "Расширение '{ext}' уже используется в категории '{conflicting_category_name}'.",
        "browse_dialog_title": "Выберите папку для сортировки",
        "cancel_button": "Отмена",
        "user_cat_add_new_label": "Добавить новую / Редактировать выбранную категорию",
        "icon_load_error_title": "Ошибка загрузки иконки",
        "icon_load_error_message": "Не удалось загрузить файл иконки: {icon_path}\nУбедитесь, что файл существует и доступен.",
        "undo_confirm_title": "Отменить последнюю сортировку?",
        "undo_confirm_message": "Вы уверены, что хотите отменить последнюю операцию сортировки для папки '{folder}'?\nЭто попытается вернуть перемещенные файлы на их исходные места.",
        "undo_no_log_title": "Нет информации для отмены",
        "undo_no_log_message": "Для папки '{folder}' не найдено информации о последней сортировке для отмены.",
        "undo_starting": "Начинаю отмену последней сортировки для папки: {folder}",
        "undo_error_reading_log": "Ошибка чтения лога отмены: {error}",
        "undo_file_restored": "Восстановлен: '{filename}' -> '{original_path}'",
        "undo_file_restore_failed": "Ошибка восстановления '{filename}' в '{original_path}': {error}",
        "undo_file_conflict_at_original": "Конфликт: Файл '{original_path}' уже существует. Восстановление '{filename}' пропущено.",
        "undo_complete": "Отмена сортировки завершена.",
        "undo_summary_restored": "Всего файлов восстановлено: {count}.",
        "undo_summary_failed": "Не удалось восстановить: {count} файл(ов).",
        "user_cat_reset_button": "Сбросить настройки категорий",
        "user_cat_reset_confirm_title": "Сбросить настройки категорий?",
        "user_cat_reset_confirm_message": "Вы уверены, что хотите сбросить все имена папок и расширения категорий к значениям по умолчанию, а также удалить все пользовательские категории?",
        "categories_internal_keys_display_names": {
            "Снимки экрана": "Снимки экрана", "Программирование Java": "Программирование Java",
            "Изображения": "Изображения", "Документы": "Документы", "Архивы": "Архивы",
            "Видео": "Видео", "Аудио": "Аудио", "Код и Текст": "Код и Текст",
            "Торренты": "Торренты", "Исполняемые файлы": "Исполняемые файлы",
            "Электронные книги": "Электронные книги", "Шрифты": "Шрифты",
            "Проекты Photoshop": "Проекты Photoshop", "Проекты Illustrator": "Проекты Illustrator",
            "Проекты Blender": "Проекты Blender", "3D Модели": "3D Модели",
            "ГИС Данные": "ГИС Данные", "Другое": "Другое"
        },
        "default_folder_names_on_disk": {
            "Снимки экрана": "Снимки экрана", "Программирование Java": "Программирование Java",
            "Изображения": "Изображения", "Документы": "Документы", "Архивы": "Архивы",
            "Видео": "Видео", "Аудио": "Аудио", "Код и Текст": "Код и Текст",
            "Торренты": "Торренты", "Исполняемые файлы": "Исполняемые файлы",
            "Электронные книги": "Электронные книги", "Шрифты": "Шрифты",
            "Проекты Photoshop": "Проекты Photoshop", "Проекты Illustrator": "Проекты Illustrator",
            "Проекты Blender": "Проекты Blender", "3D Модели": "3D Модели",
            "ГИС Данные": "ГИС Данные", "Другое": "Другое"
        },
        "java_subfolder_names_on_disk": {
            "Исходники Java": "Исходники Java", "Классы Java": "Классы Java", "JAR-архивы": "JAR-архивы"
        }
    },
    "en": {
        "title": "File Organizer v1.0 pre1 - English",
        "browse_folder_label": "Folder to sort:", "browse_button": "Browse...",
        "open_folder_button": "Open Folder",
        "undo_last_sort_button": "Undo Last Sort",
        "categories_label": "Categories to sort",
        "select_all_button": "Select All", "deselect_all_button": "Deselect All",
        "options_label": "Additional Options",
        "dry_run_checkbox": "Dry Run (preview changes, no files moved)",
        "organize_by_date_checkbox": "Create<y_bin_358>/MM subfolders within categories (by modification date)",
        "conflict_label": "On name conflict:",
        "conflict_rename": "Rename (1,2,3...)", "conflict_skip": "Skip file",
        "start_button_idle": "Start Organization", "start_button_busy": "Organizing...",
        "log_label": "Operation Log:",
        "info_label_template": "File Organizer v1.0 pre1 by IQUXAe",
        "error_no_folder_selected_title": "Error",
        "error_no_folder_selected_message": "Please select a folder to organize.",
        "error_critical_title": "Critical Error",
        "error_critical_message_template": "An unexpected error occurred: {error}",
        "info_completed_title": "Completed",
        "info_completed_message": "File organization is complete!",
        "log_starting_organization": "Starting file organization in directory: {directory}",
        "log_dry_run_active": "DRY RUN MODE: Files will not be moved.",
        "log_date_organization_active": "'Organize by Date (YYYY/MM)' option is active.",
        "log_conflict_resolution_strategy": "Name conflict resolution strategy: {strategy}",
        "log_folder_created": "Created folder: {folder}",
        "log_error_creating_folder": "Error creating folder {folder}: {error}",
        "log_skipping_file_exists_conflict": "Skipping: File '{filename}' already exists in '{category_path_on_disk}' and will be skipped.",
        "log_renaming_file_conflict": "Conflict: File '{original_filename}' will be renamed to '{new_filename}' in folder '{category_path_on_disk}'.",
        "log_moving_file": "{action_prefix}Moving: '{filename}' -> '{category_path_on_disk}/{new_filename}'",
        "log_error_moving_file": "Error moving file '{filename}': {error}",
        "log_total_files_action": "Total files {action}: {count}",
        "log_action_analyzed": "analyzed",
        "log_action_moved": "processed and moved",
        "log_no_new_files": "No new files found to analyze/move, or all suitable files are already sorted.",
        "log_organization_complete": "File organization complete.",
        "log_summary_moved_to": "Moved to '{category_folder_name}': {count} file(s).",
        "log_summary_no_files_moved": "No files were moved.",
        "log_folder_selected": "Selected folder: {folder}",
        "log_date_warning_template": "Warning: Could not get date for file '{filename}', it will not be sorted by date. Error: {error}",
        "log_skipping_ignored_folder": "Skipping ignored folder: {folder_name}",
        "log_skipping_category_folder": "Skipping category folder: {folder_name}",
        "language_label": "Language (Язык):",
        "program_settings_label": "Program Settings:",
        "settings_saved_title": "Settings Saved",
        "settings_saved_message": "Current settings have been automatically saved.",
        "settings_load_error_title": "Error Loading Settings",
        "settings_load_error_message": "Failed to load settings from: {filepath}\nError: {error}",
        "settings_file_not_found": "Settings file not found: {filepath}",
        "settings_file_filter_name": "Settings Files",
        "warning_pre_sort_title": "Attention Before Sorting!",
        "warning_pre_sort_message": "Before starting file organization, please ensure that:\n1. All files in the selected folder ({folder}) are closed in all programs.\n2. You have not selected the folder containing this or other important system/program files for sorting.\n\nProceed?",
        "error_sorting_program_folder_title": "Security Error",
        "error_sorting_program_folder_message": "You are attempting to sort the folder where File Organizer itself is located, or its parent folder. This action is prohibited to prevent program corruption.\n\nPlease choose a different folder.",
        "customize_categories_button": "Customize Categories...",
        "user_categories_title": "Customize Categories",
        "user_cat_folder_name_label": "Folder Name on Disk:",
        "user_cat_extensions_label": "Extensions (comma-separated, e.g. .aaa,.bbb):",
        "user_cat_add_button": "Add (User-defined)",
        "user_cat_edit_button": "Edit Selected",
        "user_cat_update_button": "Update Category",
        "user_cat_cancel_edit_button": "Cancel Edit",
        "user_cat_remove_button": "Remove (User-defined)",
        "user_cat_save_close_button": "OK (Save Changes)",
        "user_cat_list_label": "Sort Categories (Standard & User-defined):",
        "user_cat_info_delete": "Note: Folder name on disk and extensions can be changed for all categories. User-defined categories can be deleted.",
        "user_cat_empty_name_error_title": "Error",
        "user_cat_empty_name_error_message": "Category folder name cannot be empty.",
        "user_cat_empty_ext_error_message": "Extensions list cannot be empty. Please provide at least one extension (e.g. .txt).",
        "user_cat_invalid_ext_error_message": "Extensions must start with a dot (e.g. .txt, .docx).",
        "user_cat_name_exists_error_message": "A category with folder name '{folder_name}' already exists.",
        "user_cat_extension_conflict_error_message": "Extension '{ext}' is already used in category '{conflicting_category_name}'.",
        "browse_dialog_title": "Select Folder to Organize",
        "cancel_button": "Cancel",
        "user_cat_add_new_label": "Add New / Edit Selected Category",
        "icon_load_error_title": "Icon Load Error",
        "icon_load_error_message": "Failed to load the icon file: {icon_path}\nPlease ensure the file exists and is accessible.",
        "undo_confirm_title": "Undo Last Sort?",
        "undo_confirm_message": "Are you sure you want to undo the last sort operation for the folder '{folder}'?\nThis will attempt to move files back to their original locations.",
        "undo_no_log_title": "Nothing to Undo",
        "undo_no_log_message": "No information found about the last sort operation for folder '{folder}' to undo.",
        "undo_starting": "Starting undo of the last sort for folder: {folder}",
        "undo_error_reading_log": "Error reading undo log: {error}",
        "undo_file_restored": "Restored: '{filename}' -> '{original_path}'",
        "undo_file_restore_failed": "Failed to restore '{filename}' to '{original_path}': {error}",
        "undo_file_conflict_at_original": "Conflict: File '{original_path}' already exists. Restore of '{filename}' skipped.",
        "undo_complete": "Undo operation complete.",
        "undo_summary_restored": "Total files restored: {count}.",
        "undo_summary_failed": "Failed to restore: {count} file(s).",
        "user_cat_reset_button": "Reset Category Settings",
        "user_cat_reset_confirm_title": "Reset Category Settings?",
        "user_cat_reset_confirm_message": "Are you sure you want to reset all category folder names and extensions to their default values, and delete all user-defined categories?",
        "categories_internal_keys_display_names": {
            "Снимки экрана": "Screenshots", "Программирование Java": "Java Programming",
            "Изображения": "Images", "Документы": "Documents", "Архивы": "Archives",
            "Видео": "Videos", "Аудио": "Audio", "Код и Текст": "Code & Text",
            "Торренты": "Torrents", "Исполняемые файлы": "Executables",
            "Электронные книги": "E-books", "Шрифты": "Fonts",
            "Проекты Photoshop": "Photoshop Projects", "Проекты Illustrator": "Illustrator Projects",
            "Проекты Blender": "Blender Projects", "3D Модели": "3D Models",
            "ГИС Данные": "GIS Data", "Другое": "Other"
        },
        "default_folder_names_on_disk": {
            "Снимки экрана": "Screenshots", "Программирование Java": "Java Programming",
            "Изображения": "Images", "Документы": "Documents", "Архивы": "Archives",
            "Видео": "Videos", "Аудио": "Audio", "Код и Текст": "Code & Text",
            "Торренты": "Torrents", "Исполняемые файлы": "Executables",
            "Электронные книги": "E-books", "Шрифты": "Fonts",
            "Проекты Photoshop": "Photoshop Projects", "Проекты Illustrator": "Illustrator Projects",
            "Проекты Blender": "Blender Projects", "3D Модели": "3D Models",
            "ГИС Данные": "GIS Data", "Другое": "Other"
        },
        "java_subfolder_names_on_disk": {
            "Исходники Java": "Java Source Files", "Классы Java": "Java Class Files", "JAR-архивы": "JAR Archives"
        }
    }
}
CIS_LANG_CODES_PREFIXES = ['ru', 'uk', 'be', 'kk', 'uz', 'az', 'hy', 'ka', 'ky', 'tg', 'tk', 'mo']
CONFIG_FILE_NAME = "file_organizer_settings.ini"
DEFAULT_ICON_NAME = "app_icon.png"
UNDO_LOG_FILE_NAME = "_undo_log.json"

SCREENSHOT_INTERNAL_KEY = "Снимки экрана"
SCREENSHOT_KEYWORDS = [
    "снимок экрана", "скриншот", "screenshot", "capture", "запись экрана",
    "экран", "printscreen", "scrn", "snapshot"
]
JAVA_INTERNAL_KEY = "Программирование Java"
JAVA_SUBFOLDERS_INTERNAL_KEYS_MAP = {
    ".java": "Исходники Java", ".class": "Классы Java", ".jar": "JAR-архивы"
}
JAVA_EXTENSIONS = list(JAVA_SUBFOLDERS_INTERNAL_KEYS_MAP.keys())
DEFAULT_CATEGORY_EXTENSIONS_MAP = {
    "Изображения": [".jpg", ".jpeg", ".png", ".gif", ".bmp", ".tiff", ".svg", ".webp", ".heic", ".ico"],
    "Документы": [".pdf", ".doc", ".docx", ".xls", ".xlsx", ".ppt", ".pptx", ".txt", ".rtf", ".odt", ".ods", ".odp", ".csv", ".pps", ".key"],
    "Архивы": [".zip", ".rar", ".tar", ".gz", ".7z", ".bz2", ".iso", ".img"],
    "Видео": [".mp4", ".mov", ".avi", ".mkv", ".wmv", ".flv", ".webm", ".mpeg", ".mpg", ".m4v"],
    "Аудио": [".mp3", ".wav", ".ogg", ".flac", ".aac", ".m4a", ".wma"],
    "Код и Текст": [".py", ".js", ".html", ".css", ".c", ".cpp", ".h", ".hpp", ".json", ".xml", ".md", ".sh", ".bat", ".rb", ".php", ".go", ".swift", ".kt", ".kts", ".yaml", ".yml", ".ini", ".cfg", ".conf", ".toml"],
    "Торренты": [".torrent"],
    "Исполняемые файлы": [".exe", ".msi", ".dmg", ".app", ".deb", ".rpm"],
    "Электронные книги": [".epub", ".mobi", ".azw", ".azw3", ".fb2", ".lit", ".lrf"],
    "Шрифты": [".ttf", ".otf", ".woff", ".woff2", ".eot"],
    "Проекты Photoshop": [".psd", ".psb"],
    "Проекты Illustrator": [".ai", ".eps"],
    "Проекты Blender": [".blend"],
    "3D Модели": [".obj", ".stl", ".fbx", ".dae", ".3ds"],
    "ГИС Данные": [".shp", ".geojson", ".kml", ".gpx"],
    "Другое": []
}
DEFAULT_IGNORED_FOLDERS = {'.git', '.svn', 'node_modules', '__pycache__', '.vscode', '.idea', '$recycle.bin', 'system volume information'}
ALL_DEFAULT_CATEGORY_INTERNAL_KEYS = sorted(list(set([SCREENSHOT_INTERNAL_KEY, JAVA_INTERNAL_KEY] + list(DEFAULT_CATEGORY_EXTENSIONS_MAP.keys()))))

def get_script_directory():
    if getattr(sys, 'frozen', False): return os.path.dirname(sys.executable)
    else: return os.path.dirname(os.path.abspath(__file__))

def get_system_language():
    try:
        lang_code, _ = locale.getdefaultlocale()
        if lang_code:
            prefix = lang_code.split('_')[0].lower()
            if prefix in CIS_LANG_CODES_PREFIXES: return "ru"
    except Exception: pass
    return "en"

def log_message(text_area, message, strings=None, msg_key=None, **kwargs):
    final_message = message
    if strings and msg_key and msg_key in strings:
        try: final_message = strings[msg_key].format(**kwargs)
        except KeyError: final_message = strings[msg_key]
    if text_area:
        try:
            if text_area.winfo_exists():
                text_area.insert(tk.END, final_message + "\n")
                text_area.see(tk.END)
        except tk.TclError: print(f"Log (TclError): {final_message}")
    else: print(final_message)

def _move_file_to_category(source_file_path, original_item_name, target_category_path_on_disk, base_directory_path,
                           logger_func_ref, current_strings, dry_run=False, organize_by_date=False, conflict_resolution="rename"):
    final_target_path_segment = target_category_path_on_disk
    operation_details = None

    if organize_by_date:
        try:
            mod_time = os.path.getmtime(source_file_path)
            date_obj = datetime.fromtimestamp(mod_time)
            year_str = date_obj.strftime("%Y")
            month_str = date_obj.strftime("%m")
            final_target_path_segment = os.path.join(target_category_path_on_disk, year_str, month_str)
        except Exception as e:
            logger_func_ref("log_date_warning_template", filename=original_item_name, error=e)

    destination_folder_abs = os.path.join(base_directory_path, final_target_path_segment)

    if not dry_run and not os.path.exists(destination_folder_abs):
        try:
            os.makedirs(destination_folder_abs, exist_ok=True)
            logger_func_ref("log_folder_created", folder=destination_folder_abs)
        except OSError as e:
            logger_func_ref("log_error_creating_folder", folder=destination_folder_abs, error=e)
            return False, None

    destination_file_abs = os.path.join(destination_folder_abs, original_item_name)

    if os.path.abspath(source_file_path) == os.path.abspath(destination_file_abs): return False, None

    final_destination_item_name_on_disk = original_item_name
    if os.path.exists(destination_file_abs):
        if conflict_resolution == "skip":
            logger_func_ref("log_skipping_file_exists_conflict", filename=original_item_name, category_path_on_disk=final_target_path_segment)
            return False, None
        elif conflict_resolution == "rename":
            file_name_part, file_extension_part = os.path.splitext(original_item_name)
            counter = 1
            while os.path.exists(destination_file_abs):
                final_destination_item_name_on_disk = f"{file_name_part} ({counter}){file_extension_part}"
                destination_file_abs = os.path.join(destination_folder_abs, final_destination_item_name_on_disk)
                counter += 1
            if original_item_name != final_destination_item_name_on_disk:
                 logger_func_ref("log_renaming_file_conflict", original_filename=original_item_name, new_filename=final_destination_item_name_on_disk, category_path_on_disk=final_target_path_segment)

    action_prefix = "[DRY RUN] " if dry_run else ""
    logger_func_ref("log_moving_file", action_prefix=action_prefix, filename=original_item_name, category_path_on_disk=final_target_path_segment, new_filename=final_destination_item_name_on_disk)

    if not dry_run:
        try:
            shutil.move(source_file_path, destination_file_abs)
            operation_details = {
                'source_abs': source_file_path,
                'dest_abs': destination_file_abs,
                'target_category_folder_name_on_disk': target_category_path_on_disk
            }
            return True, operation_details
        except Exception as e:
            logger_func_ref("log_error_moving_file", filename=original_item_name, error=e)
            return False, None

    operation_details = {
        'source_abs': source_file_path,
        'dest_abs': destination_file_abs,
        'target_category_folder_name_on_disk': target_category_path_on_disk
    }
    return True, operation_details


def organize_files(directory_path, active_categories_config_map,
                   current_user_defined_categories, current_default_category_configs,
                   text_area_widget=None, current_strings=None,
                   dry_run=False, organize_by_date=False, conflict_resolution="rename"):

    logger_with_strings = lambda msg_key, **kwargs: log_message(text_area_widget, None, current_strings, msg_key, **kwargs)
    moved_files_summary = {}
    undo_log_operations = []


    if not os.path.isdir(directory_path):
        logger_with_strings("error_no_folder_selected_message"); return moved_files_summary, undo_log_operations

    logger_with_strings("log_starting_organization", directory=directory_path)
    if dry_run: logger_with_strings("log_dry_run_active")
    if organize_by_date: logger_with_strings("log_date_organization_active")

    strategy_display = current_strings.get("conflict_rename") if conflict_resolution == "rename" else current_strings.get("conflict_skip", "unknown")
    logger_with_strings("log_conflict_resolution_strategy", strategy=strategy_display)

    files_processed_count = 0

    all_managed_folder_names_on_disk = set()
    for def_cat_config in current_default_category_configs.values():
        all_managed_folder_names_on_disk.add(def_cat_config['folder_name_on_disk'])
        if def_cat_config['internal_key'] == JAVA_INTERNAL_KEY:
            java_main_folder_on_disk = def_cat_config['folder_name_on_disk']
            java_subfolder_names_map_for_check = def_cat_config.get('subfolder_names_on_disk', current_strings["java_subfolder_names_on_disk"])
            for sub_folder_name_on_disk in java_subfolder_names_map_for_check.values():
                 all_managed_folder_names_on_disk.add(os.path.join(java_main_folder_on_disk, sub_folder_name_on_disk))


    for user_cat in current_user_defined_categories:
        all_managed_folder_names_on_disk.add(user_cat['folder_name_on_disk'])


    for item_name_on_disk in os.listdir(directory_path):
        item_path_abs = os.path.join(directory_path, item_name_on_disk)

        if item_name_on_disk.startswith('.'): continue
        if os.path.isdir(item_path_abs):
            if item_name_on_disk.lower() in DEFAULT_IGNORED_FOLDERS:
                logger_with_strings("log_skipping_ignored_folder", folder_name=item_name_on_disk); continue
            if item_name_on_disk in all_managed_folder_names_on_disk:
                 logger_with_strings("log_skipping_category_folder", folder_name=item_name_on_disk); continue
            continue

        file_name_part, file_extension = os.path.splitext(item_name_on_disk)
        file_extension_lower = file_extension.lower()
        file_name_lower_no_ext = file_name_part.lower()

        target_category_path_on_disk_for_file = None

        for user_cat in current_user_defined_categories:
            if active_categories_config_map.get(user_cat['id'], False):
                user_cat_extensions = [ext.strip().lower() for ext in user_cat['extensions']]
                if file_extension_lower in user_cat_extensions:
                    target_category_path_on_disk_for_file = user_cat['folder_name_on_disk']
                    break
        if target_category_path_on_disk_for_file:
            moved, op_details = _move_file_to_category(item_path_abs, item_name_on_disk, target_category_path_on_disk_for_file, directory_path,
                                      logger_with_strings, current_strings, dry_run, organize_by_date, conflict_resolution)
            if moved:
                files_processed_count += 1
                if op_details:
                    undo_log_operations.append(op_details)
                    cat_name_for_summary = op_details['target_category_folder_name_on_disk']
                    moved_files_summary[cat_name_for_summary] = moved_files_summary.get(cat_name_for_summary, 0) + 1
            continue

        if active_categories_config_map.get(SCREENSHOT_INTERNAL_KEY, False):
            if any(keyword in file_name_lower_no_ext for keyword in SCREENSHOT_KEYWORDS):
                target_category_path_on_disk_for_file = current_default_category_configs.get(SCREENSHOT_INTERNAL_KEY, {}).get('folder_name_on_disk')

        if not target_category_path_on_disk_for_file and active_categories_config_map.get(JAVA_INTERNAL_KEY, False) and file_extension_lower in JAVA_EXTENSIONS:
            java_cat_config = current_default_category_configs.get(JAVA_INTERNAL_KEY, {})
            java_main_folder_on_disk = java_cat_config.get('folder_name_on_disk')
            if java_main_folder_on_disk:
                internal_java_subfolder_key = JAVA_SUBFOLDERS_INTERNAL_KEYS_MAP.get(file_extension_lower)
                if internal_java_subfolder_key:
                    actual_sub_name = java_cat_config.get('subfolder_names_on_disk', {}).get(internal_java_subfolder_key,
                                                                                             current_strings["java_subfolder_names_on_disk"].get(internal_java_subfolder_key, internal_java_subfolder_key))
                    target_category_path_on_disk_for_file = os.path.join(java_main_folder_on_disk, actual_sub_name)

        if not target_category_path_on_disk_for_file:
            for internal_key, def_cat_config in current_default_category_configs.items():
                if internal_key == "Другое": continue
                if active_categories_config_map.get(internal_key, False) and file_extension_lower in def_cat_config.get('extensions', []):
                    target_category_path_on_disk_for_file = def_cat_config.get('folder_name_on_disk')
                    break

        if not target_category_path_on_disk_for_file and active_categories_config_map.get("Другое", False):
            target_category_path_on_disk_for_file = current_default_category_configs.get("Другое", {}).get('folder_name_on_disk')

        if target_category_path_on_disk_for_file:
            moved, op_details = _move_file_to_category(item_path_abs, item_name_on_disk, target_category_path_on_disk_for_file, directory_path,
                                      logger_with_strings, current_strings, dry_run, organize_by_date, conflict_resolution)
            if moved:
                files_processed_count += 1
                if op_details:
                    undo_log_operations.append(op_details)
                    cat_name_for_summary = op_details['target_category_folder_name_on_disk']
                    moved_files_summary[cat_name_for_summary] = moved_files_summary.get(cat_name_for_summary, 0) + 1

    action_str = current_strings.get("log_action_analyzed" if dry_run else "log_action_moved", "processed")
    if files_processed_count > 0:
        logger_with_strings("log_total_files_action", action=action_str, count=files_processed_count)
    else:
        logger_with_strings("log_no_new_files")
    logger_with_strings("log_organization_complete")

    if not dry_run and undo_log_operations:
        undo_log_path = os.path.join(directory_path, UNDO_LOG_FILE_NAME)
        try:
            with open(undo_log_path, 'w', encoding='utf-8') as f:
                json.dump({"operations": undo_log_operations, "timestamp": datetime.now().isoformat()}, f, ensure_ascii=False, indent=4)
        except Exception as e:
            logger_with_strings("log_error_creating_folder", folder=f"undo log ({undo_log_path})", error=e)


    if text_area_widget and not dry_run and files_processed_count > 0 :
        try:
            if text_area_widget.winfo_exists():
                 messagebox.showinfo(current_strings.get("info_completed_title", "Completed"),
                                     current_strings.get("info_completed_message", "File organization is complete!"))
        except tk.TclError: pass
    return moved_files_summary, undo_log_operations


class UserCategoriesDialog(simpledialog.Dialog):
    def __init__(self, parent, title, app_strings,
                 current_user_categories_list,
                 current_default_category_configs_dict,
                 all_default_category_internal_keys_list,
                 original_default_extensions_map,
                 original_default_folder_names_map,
                 original_java_subfolder_names_map):
        self.app_strings = app_strings
        self.user_categories_temp = [dict(cat) for cat in current_user_categories_list]
        self.default_category_configs_temp = {k: dict(v) for k, v in current_default_category_configs_dict.items()}

        self.all_default_category_internal_keys = all_default_category_internal_keys_list
        self.original_default_extensions_map = original_default_extensions_map
        self.original_default_folder_names_map = original_default_folder_names_map
        self.original_java_subfolder_names_map = original_java_subfolder_names_map


        self.listbox = None
        self.folder_name_entry = None
        self.extensions_entry = None
        self.editing_category_info = None
        super().__init__(parent, title=title)

    def body(self, master):
        master.pack_configure(fill=tk.BOTH, expand=True)
        master.columnconfigure(0, weight=1)
        master.rowconfigure(1, weight=1)

        self.edit_controls_frame = ttk.LabelFrame(master, text=self.app_strings.get("user_cat_add_new_label", "Add/Edit Category"))
        self.edit_controls_frame.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        self.edit_controls_frame.columnconfigure(1, weight=1)

        ttk.Label(self.edit_controls_frame, text=self.app_strings.get("user_cat_folder_name_label", "Имя папки на диске:")).grid(row=0, column=0, padx=5, pady=2, sticky="w")
        self.folder_name_entry = ttk.Entry(self.edit_controls_frame, width=40)
        self.folder_name_entry.grid(row=0, column=1, padx=5, pady=2, sticky="ew")

        ttk.Label(self.edit_controls_frame, text=self.app_strings.get("user_cat_extensions_label", "Расширения (.ext1,.ext2):")).grid(row=1, column=0, padx=5, pady=2, sticky="w")
        self.extensions_entry = ttk.Entry(self.edit_controls_frame, width=40)
        self.extensions_entry.grid(row=1, column=1, padx=5, pady=2, sticky="ew")

        self.action_button_frame = ttk.Frame(self.edit_controls_frame)
        self.action_button_frame.grid(row=0, column=2, rowspan=2, padx=5, pady=2, sticky="ns")

        self.add_or_update_btn = ttk.Button(self.action_button_frame, command=self.add_or_update_category)
        self.add_or_update_btn.pack(pady=2, fill=tk.X)
        self.cancel_edit_btn = ttk.Button(self.action_button_frame, text=self.app_strings.get("user_cat_cancel_edit_button", "Отменить ред."), command=self.cancel_edit_mode)
        self.cancel_edit_btn.pack(pady=2, fill=tk.X)


        list_management_frame = ttk.Frame(master)
        list_management_frame.grid(row=1, column=0, padx=10, pady=5, sticky="nsew")
        list_management_frame.columnconfigure(0, weight=1)
        list_management_frame.rowconfigure(0, weight=1)

        self.listbox = tk.Listbox(list_management_frame, height=10, exportselection=False)
        self.listbox.grid(row=0, column=0, padx=(0,5), pady=5, sticky="nsew")

        scrollbar = ttk.Scrollbar(list_management_frame, orient="vertical", command=self.listbox.yview)
        scrollbar.grid(row=0, column=1, sticky="ns", pady=5)
        self.listbox.config(yscrollcommand=scrollbar.set)
        self.listbox.bind("<<ListboxSelect>>", self.on_listbox_select)

        list_buttons_frame = ttk.Frame(list_management_frame)
        list_buttons_frame.grid(row=1, column=0, columnspan=2, pady=5)

        self.edit_btn = ttk.Button(list_buttons_frame, text=self.app_strings.get("user_cat_edit_button", "Редактировать"), command=self.start_edit_mode, state=tk.DISABLED)
        self.edit_btn.pack(side=tk.LEFT, padx=5)
        self.remove_btn = ttk.Button(list_buttons_frame, text=self.app_strings.get("user_cat_remove_button", "Удалить (польз.)"), command=self.remove_user_category, state=tk.DISABLED)
        self.remove_btn.pack(side=tk.LEFT, padx=5)
        self.reset_all_btn = ttk.Button(list_buttons_frame, text=self.app_strings.get("user_cat_reset_button", "Сбросить"), command=self.reset_all_category_settings)
        self.reset_all_btn.pack(side=tk.LEFT, padx=5)


        self.populate_listbox()
        self.cancel_edit_mode()

        ttk.Label(master, text=self.app_strings.get("user_cat_info_delete", "Примечание: ..."), wraplength=480, justify=tk.LEFT).grid(row=2, column=0, padx=10, pady=5, sticky="w")

        return self.folder_name_entry

    def on_listbox_select(self, event=None):
        has_selection = bool(self.listbox.curselection())
        can_edit = has_selection and self.editing_category_info is None

        can_remove = False
        if can_edit:
            idx = self.listbox.curselection()[0]
            if idx >= len(self.all_default_category_internal_keys):
                can_remove = True

        self.edit_btn.config(state=tk.NORMAL if can_edit else tk.DISABLED)
        self.remove_btn.config(state=tk.NORMAL if can_remove else tk.DISABLED)


    def populate_listbox(self):
        self.listbox.delete(0, tk.END)

        for internal_key in self.all_default_category_internal_keys:
            config = self.default_category_configs_temp.get(internal_key, {})
            folder_name_on_disk = config.get('folder_name_on_disk', self.original_default_folder_names_map.get(internal_key, internal_key))
            extensions = config.get('extensions', self.original_default_extensions_map.get(internal_key, []))
            original_ui_name = self.app_strings["categories_internal_keys_display_names"].get(internal_key, internal_key)
            
            display_text_for_listbox = folder_name_on_disk
            if folder_name_on_disk != original_ui_name:
                display_text_for_listbox = f"{folder_name_on_disk} ({original_ui_name})"

            ext_str = ", ".join(extensions)
            self.listbox.insert(tk.END, f"[S] {display_text_for_listbox}: {ext_str}")

        for cat in self.user_categories_temp:
            ext_str = ", ".join(cat.get('extensions', []))
            self.listbox.insert(tk.END, f"[U] {cat.get('folder_name_on_disk', 'Unnamed')}: {ext_str}")
        self.on_listbox_select()

    def _validate_inputs_and_check_conflicts(self, proposed_folder_name, proposed_extensions_str, editing_id_or_key=None, is_default_being_edited=False):
        if not proposed_folder_name:
            messagebox.showerror(self.app_strings.get("user_cat_empty_name_error_title", "Error"),
                                 self.app_strings.get("user_cat_empty_name_error_message", "Folder name cannot be empty."), parent=self)
            return None, None
        if not proposed_extensions_str:
            messagebox.showerror(self.app_strings.get("user_cat_empty_name_error_title", "Error"),
                                 self.app_strings.get("user_cat_empty_ext_error_message", "Extensions list cannot be empty."), parent=self)
            return None, None

        parsed_extensions = [ext.strip().lower() for ext in proposed_extensions_str.split(',') if ext.strip()]
        if not all(ext.startswith('.') for ext in parsed_extensions):
            messagebox.showerror(self.app_strings.get("user_cat_empty_name_error_title", "Error"),
                                 self.app_strings.get("user_cat_invalid_ext_error_message", "Extensions must start with a dot."), parent=self)
            return None, None
        if not parsed_extensions:
             messagebox.showerror(self.app_strings.get("user_cat_empty_name_error_title", "Error"),
                                 self.app_strings.get("user_cat_empty_ext_error_message", "Provide valid extensions."), parent=self)
             return None, None

        all_current_folder_names = []
        for def_key, def_conf in self.default_category_configs_temp.items():
            if is_default_being_edited and def_key == editing_id_or_key: continue
            all_current_folder_names.append(def_conf['folder_name_on_disk'])
        for user_c in self.user_categories_temp:
            if not is_default_being_edited and user_c.get('id') == editing_id_or_key: continue
            all_current_folder_names.append(user_c['folder_name_on_disk'])

        if proposed_folder_name in all_current_folder_names:
            messagebox.showerror(self.app_strings.get("user_cat_empty_name_error_title", "Error"),
                                 self.app_strings.get("user_cat_name_exists_error_message", "Folder name exists.").format(folder_name=proposed_folder_name), parent=self)
            return None, None

        for ext_to_check in parsed_extensions:
            for def_key, def_conf in self.default_category_configs_temp.items():
                if is_default_being_edited and def_key == editing_id_or_key: continue
                if ext_to_check in def_conf.get('extensions', []):
                    conflicting_display_name = self.app_strings["categories_internal_keys_display_names"].get(def_key, def_key)
                    messagebox.showerror(self.app_strings.get("user_cat_empty_name_error_title", "Error"),
                                         self.app_strings.get("user_cat_extension_conflict_error_message", "Ext conflict.")
                                         .format(ext=ext_to_check, conflicting_category_name=conflicting_display_name), parent=self)
                    return None, None
            for user_c in self.user_categories_temp:
                if not is_default_being_edited and user_c.get('id') == editing_id_or_key: continue
                if ext_to_check in user_c.get('extensions', []):
                     messagebox.showerror(self.app_strings.get("user_cat_empty_name_error_title", "Error"),
                                         self.app_strings.get("user_cat_extension_conflict_error_message", "Ext conflict.")
                                         .format(ext=ext_to_check, conflicting_category_name=user_c['folder_name_on_disk']), parent=self)
                     return None, None

        return proposed_folder_name, parsed_extensions


    def add_or_update_category(self):
        folder_name_from_entry = self.folder_name_entry.get().strip()
        extensions_str = self.extensions_entry.get().strip()

        editing_id_or_key = None
        is_default_edit = False
        if self.editing_category_info:
            editing_id_or_key = self.editing_category_info['id_or_key']
            is_default_edit = self.editing_category_info['is_default']

        validated_folder_name, validated_extensions = self._validate_inputs_and_check_conflicts(
            folder_name_from_entry, extensions_str, editing_id_or_key, is_default_edit
        )

        if not validated_folder_name or not validated_extensions:
            return

        if self.editing_category_info is None:
            new_id = str(uuid.uuid4())
            self.user_categories_temp.append({
                'id': new_id,
                'folder_name_on_disk': validated_folder_name,
                'extensions': validated_extensions
            })
        elif self.editing_category_info:
            cat_id_or_key_to_update = self.editing_category_info['id_or_key']
            is_default_to_update = self.editing_category_info['is_default']

            if is_default_to_update:
                if cat_id_or_key_to_update in self.default_category_configs_temp:
                    self.default_category_configs_temp[cat_id_or_key_to_update]['folder_name_on_disk'] = validated_folder_name
                    self.default_category_configs_temp[cat_id_or_key_to_update]['extensions'] = validated_extensions
            else:
                for i, cat in enumerate(self.user_categories_temp):
                    if cat.get('id') == cat_id_or_key_to_update:
                        self.user_categories_temp[i]['folder_name_on_disk'] = validated_folder_name
                        self.user_categories_temp[i]['extensions'] = validated_extensions
                        break
        self.populate_listbox()
        self.cancel_edit_mode()

    def start_edit_mode(self):
        selected_indices = self.listbox.curselection()
        if not selected_indices: return

        idx = selected_indices[0]
        self.editing_category_info = {'listbox_index': idx}

        current_folder_name = ""
        current_extensions_list = []

        if idx < len(self.all_default_category_internal_keys):
            internal_key = self.all_default_category_internal_keys[idx]
            self.editing_category_info['id_or_key'] = internal_key
            self.editing_category_info['is_default'] = True

            config = self.default_category_configs_temp.get(internal_key, {})
            current_folder_name = config.get('folder_name_on_disk', self.original_default_folder_names_map.get(internal_key, internal_key))
            current_extensions_list = config.get('extensions', self.original_default_extensions_map.get(internal_key, []))
            self.folder_name_entry.config(state='normal')
        else:
            user_cat_idx = idx - len(self.all_default_category_internal_keys)
            if 0 <= user_cat_idx < len(self.user_categories_temp):
                category_to_edit = self.user_categories_temp[user_cat_idx]
                self.editing_category_info['id_or_key'] = category_to_edit.get('id')
                self.editing_category_info['is_default'] = False
                current_folder_name = category_to_edit.get('folder_name_on_disk', '')
                current_extensions_list = category_to_edit.get('extensions', [])
                self.folder_name_entry.config(state='normal')
            else:
                self.cancel_edit_mode()
                return


        self.folder_name_entry.delete(0, tk.END)
        self.folder_name_entry.insert(0, current_folder_name)
        self.extensions_entry.delete(0, tk.END)
        self.extensions_entry.insert(0, ", ".join(current_extensions_list))

        self.add_or_update_btn.config(text=self.app_strings.get("user_cat_update_button", "Update"))
        self.cancel_edit_btn.pack(pady=2, fill=tk.X, after=self.add_or_update_btn)

        self.edit_btn.config(state=tk.DISABLED)
        self.remove_btn.config(state=tk.DISABLED)
        self.reset_all_btn.config(state=tk.DISABLED)
        self.listbox.config(state=tk.DISABLED)


    def cancel_edit_mode(self):
        self.editing_category_info = None
        self.folder_name_entry.config(state='normal')
        self.folder_name_entry.delete(0, tk.END)
        self.extensions_entry.delete(0, tk.END)

        self.add_or_update_btn.config(text=self.app_strings.get("user_cat_add_button", "Add (User)"))
        self.cancel_edit_btn.pack_forget()

        self.listbox.config(state=tk.NORMAL)
        self.reset_all_btn.config(state=tk.NORMAL)
        self.on_listbox_select()


    def remove_user_category(self):
        selected_indices = self.listbox.curselection()
        if not selected_indices: return

        idx = selected_indices[0]
        if idx >= len(self.all_default_category_internal_keys):
            user_cat_list_idx_to_remove = idx - len(self.all_default_category_internal_keys)
            if 0 <= user_cat_list_idx_to_remove < len(self.user_categories_temp):
                del self.user_categories_temp[user_cat_list_idx_to_remove]
                self.populate_listbox()
        self.cancel_edit_mode()

    def reset_all_category_settings(self):
        if not messagebox.askyesno(
            self.app_strings.get("user_cat_reset_confirm_title", "Confirm Reset"),
            self.app_strings.get("user_cat_reset_confirm_message", "Are you sure?"),
            parent=self):
            return

        self.default_category_configs_temp = {}
        for key in self.all_default_category_internal_keys:
            folder_name = self.original_default_folder_names_map.get(key, key)
            extensions = list(self.original_default_extensions_map.get(key, []))
            self.default_category_configs_temp[key] = {
                'internal_key': key,
                'folder_name_on_disk': folder_name,
                'extensions': extensions
            }
            if key == JAVA_INTERNAL_KEY:
                 self.default_category_configs_temp[key]['subfolder_names_on_disk'] = dict(self.original_java_subfolder_names_map)

        self.user_categories_temp = []
        self.populate_listbox()
        self.cancel_edit_mode()


    def buttonbox(self):
        box = ttk.Frame(self)
        w = ttk.Button(box, text=self.app_strings.get("user_cat_save_close_button", "OK"), width=15, command=self.ok, default=tk.ACTIVE)
        w.pack(side=tk.LEFT, padx=5, pady=5)
        w = ttk.Button(box, text=self.app_strings.get("cancel_button", "Cancel"), width=10, command=self.cancel)
        w.pack(side=tk.LEFT, padx=5, pady=5)
        self.bind("<Return>", lambda event: self.ok())
        self.bind("<Escape>", lambda event: self.cancel())
        box.pack()

    def apply(self):
        self.result = (self.user_categories_temp, self.default_category_configs_temp)


class FileOrganizerApp:
    def __init__(self, root_window):
        self.root = root_window
        self.current_lang_code = get_system_language()
        self.strings = LANGUAGES[self.current_lang_code]
        self.script_dir = get_script_directory()

        self.user_defined_categories = []
        self.default_category_configs = {}
        self._initialize_default_category_configs()


        self.root.title(self.strings["title"])
        self.root.geometry("850x680")

        self.directory_path_var = tk.StringVar()
        self.active_categories_vars = {}
        self.dry_run_var = tk.BooleanVar(value=False)
        self.organize_by_date_var = tk.BooleanVar(value=False)
        self.conflict_resolution_var = tk.StringVar()
        self.selected_language_var = tk.StringVar(value=self.current_lang_code)

        self._build_ui()
        self._bind_auto_save_events()
        self._configure_grid_weights()
        self.root.minsize(600, 500)
        self.load_configuration(silent=True)
        self.set_app_icon()
        self.update_undo_button_state()

    def _initialize_default_category_configs(self, lang_code_for_init=None):
        if lang_code_for_init is None:
            lang_code_for_init = self.current_lang_code
        
        current_lang_strings_for_init = LANGUAGES[lang_code_for_init]
        
        self.default_category_configs.clear()
        for key in ALL_DEFAULT_CATEGORY_INTERNAL_KEYS:
            folder_name = current_lang_strings_for_init["default_folder_names_on_disk"].get(key, key)
            extensions = list(DEFAULT_CATEGORY_EXTENSIONS_MAP.get(key, [])) 
            self.default_category_configs[key] = {
                'internal_key': key,
                'folder_name_on_disk': folder_name,
                'extensions': extensions
            }
            if key == JAVA_INTERNAL_KEY:
                 self.default_category_configs[key]['subfolder_names_on_disk'] = dict(current_lang_strings_for_init["java_subfolder_names_on_disk"])


    def _bind_auto_save_events(self):
        self.selected_language_var.trace_add("write", self.auto_save_configuration_event)
        self.directory_path_var.trace_add("write", self.auto_save_configuration_event)
        self.dry_run_var.trace_add("write", self.auto_save_configuration_event)
        self.organize_by_date_var.trace_add("write", self.auto_save_configuration_event)
        self.conflict_resolution_var.trace_add("write", self.auto_save_configuration_event)


    def auto_save_configuration_event(self, *args):
        if hasattr(self, '_auto_save_job'):
            self.root.after_cancel(self._auto_save_job)
        self._auto_save_job = self.root.after(500, self.auto_save_configuration)


    def auto_save_configuration(self, show_success_message=False):
        config = configparser.ConfigParser()
        config['Settings'] = {
            'language': self.current_lang_code,
            'target_directory': self.directory_path_var.get(),
            'dry_run': str(self.dry_run_var.get()),
            'organize_by_date': str(self.organize_by_date_var.get()),
            'conflict_resolution': self.conflict_resolution_var.get()
        }
        active_vars_to_save = {key: var.get() for key, var in self.active_categories_vars.items()}
        config['ActiveCategoriesState'] = {'states_json': json.dumps(active_vars_to_save)}
        config['UserDefinedCategories'] = {'categories_json': json.dumps(self.user_defined_categories)}
        config['DefaultCategoryConfigs'] = {'configs_json': json.dumps(self.default_category_configs)}


        config_path = os.path.join(self.script_dir, CONFIG_FILE_NAME)
        try:
            with open(config_path, 'w', encoding='utf-8') as configfile: config.write(configfile)
            if show_success_message:
                messagebox.showinfo(self.strings["settings_saved_title"],
                                    self.strings["settings_saved_message"])
        except Exception as e:
            messagebox.showerror(self.strings.get("settings_load_error_title", "Error"),
                                 self.strings.get("settings_load_error_message", "Failed to save: {error}").format(filepath=config_path, error=e))


    def set_app_icon(self):
        try:
            if getattr(sys, 'frozen', False): 
                
                base_path = sys._MEIPASS
            else: # Для обычного .py скрипта
                base_path = self.script_dir
            
            icon_path = os.path.join(base_path, DEFAULT_ICON_NAME) 
            
            if os.path.exists(icon_path):
                photo = tk.PhotoImage(file=icon_path)
                self.root.iconphoto(True, photo)
            else:
               
                print(f"Файл иконки '{DEFAULT_ICON_NAME}' не найден по пути: {icon_path}")
               
                
        except tk.TclError as e:
            print(f"Ошибка TclError при установке иконки '{DEFAULT_ICON_NAME}': {e}")
            if hasattr(self, 'strings') and self.strings:
                 messagebox.showwarning(
                    self.strings.get("icon_load_error_title", "Icon Error"),
                    self.strings.get("icon_load_error_message", "Failed to load icon: {icon_path}").format(icon_path=DEFAULT_ICON_NAME) + f"\nDetails: {e}",
                    parent=self.root 
                )
        except Exception as e:
            print(f"Непредвиденная ошибка при установке иконки: {e}")
           
           

    def _configure_grid_weights(self):
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=0)
        self.root.rowconfigure(1, weight=0)
        self.root.rowconfigure(2, weight=1)
        self.root.rowconfigure(3, weight=0)
        self.root.rowconfigure(4, weight=0)
        self.root.rowconfigure(5, weight=0)
        self.root.rowconfigure(6, weight=3)
        self.root.rowconfigure(7, weight=0)

        self.categories_outer_frame.columnconfigure(0, weight=1)
        self.categories_outer_frame.rowconfigure(0, weight=1)
        self.categories_outer_frame.rowconfigure(1, weight=0)

    def _build_ui(self):
        self.top_controls_frame = tk.Frame(self.root, pady=5)
        self.top_controls_frame.grid(row=0, column=0, sticky="ew", padx=10)

        self.lang_label = tk.Label(self.top_controls_frame, padx=5)
        self.lang_label.pack(side=tk.LEFT)
        lang_options_display = {"Русский": "ru", "English": "en"}
        self.lang_combobox = ttk.Combobox(self.top_controls_frame, textvariable=self.selected_language_var,
                                          values=list(lang_options_display.keys()), state="readonly", width=15)
        self.lang_combobox.pack(side=tk.LEFT, padx=(0, 10))
        self.lang_combobox.bind("<<ComboboxSelected>>", self.change_language_and_autosave)

        self.settings_label_widget = tk.Label(self.top_controls_frame, padx=5)
        self.settings_label_widget.pack(side=tk.LEFT)

        self.customize_cat_btn = tk.Button(self.top_controls_frame, command=self.open_user_categories_dialog, padx=5)
        self.customize_cat_btn.pack(side=tk.LEFT, padx=(0,10))

        self.undo_button = tk.Button(self.top_controls_frame, command=self.start_undo_thread, state=tk.DISABLED)
        self.undo_button.pack(side=tk.LEFT)


        self.path_frame = tk.Frame(self.root)
        self.path_frame.grid(row=1, column=0, sticky="ew", padx=10, pady=(5,5))
        self.path_frame.columnconfigure(1, weight=1)
        self.path_label = tk.Label(self.path_frame, padx=5)
        self.path_label.pack(side=tk.LEFT)
        self.path_entry = tk.Entry(self.path_frame, textvariable=self.directory_path_var, state='readonly')
        self.path_entry.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=5)

        self.open_folder_btn = tk.Button(self.path_frame, command=self.open_selected_folder, state=tk.DISABLED)
        self.open_folder_btn.pack(side=tk.LEFT, padx=(0,5))

        self.browse_button = tk.Button(self.path_frame, command=self.browse_directory_and_autosave, padx=10)
        self.browse_button.pack(side=tk.LEFT)


        self.categories_outer_frame = tk.LabelFrame(self.root, padx=10, pady=10)
        self.categories_outer_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=5)
        self.canvas_categories = tk.Canvas(self.categories_outer_frame)
        self.scrollbar_categories = ttk.Scrollbar(self.categories_outer_frame, orient="vertical", command=self.canvas_categories.yview)
        self.categories_inner_frame = ttk.Frame(self.canvas_categories)
        self.categories_inner_frame.bind("<Configure>", lambda e: self.canvas_categories.configure(scrollregion=self.canvas_categories.bbox("all")))
        self.canvas_categories.create_window((0, 0), window=self.categories_inner_frame, anchor="nw")
        self.canvas_categories.configure(yscrollcommand=self.scrollbar_categories.set)
        self.canvas_categories.pack(side="left", fill="both", expand=True)
        self.scrollbar_categories.pack(side="right", fill="y")
        self.select_buttons_frame = tk.Frame(self.categories_outer_frame)
        self.select_buttons_frame.pack(fill=tk.X, pady=(5,0), side=tk.BOTTOM)
        self.select_all_btn = tk.Button(self.select_buttons_frame, command=self.select_all_categories_and_autosave)
        self.select_all_btn.pack(side=tk.LEFT, padx=5)
        self.deselect_all_btn = tk.Button(self.select_buttons_frame, command=self.deselect_all_categories_and_autosave)
        self.deselect_all_btn.pack(side=tk.LEFT, padx=5)

        self.options_frame = tk.LabelFrame(self.root, padx=10, pady=10)
        self.options_frame.grid(row=3, column=0, sticky="ew", padx=10, pady=5)
        self.dry_run_cb = ttk.Checkbutton(self.options_frame, variable=self.dry_run_var, command=self.auto_save_configuration)
        self.dry_run_cb.pack(anchor='w')
        self.organize_by_date_cb = ttk.Checkbutton(self.options_frame, variable=self.organize_by_date_var, command=self.auto_save_configuration)
        self.organize_by_date_cb.pack(anchor='w')
        self.conflict_frame = tk.Frame(self.options_frame)
        self.conflict_frame.pack(fill=tk.X, pady=(5,0))
        self.conflict_label_widget = tk.Label(self.conflict_frame)
        self.conflict_label_widget.pack(side=tk.LEFT, anchor='w')
        self.conflict_combobox = ttk.Combobox(self.conflict_frame, textvariable=self.conflict_resolution_var,
                                              state="readonly", width=25)
        self.conflict_combobox.pack(side=tk.LEFT, padx=5)
        self.conflict_combobox.bind("<<ComboboxSelected>>", self.auto_save_configuration_event)

        self.start_button = tk.Button(self.root, command=self.start_organization_thread, pady=10, bg="#4CAF50", fg="white", font=("Arial", 11, "bold"))
        self.start_button.grid(row=4, column=0, sticky="ew", padx=10, pady=10)

        self.log_label_widget = tk.Label(self.root, font=("Arial", 10, "underline"))
        self.log_label_widget.grid(row=5, column=0, sticky="w", padx=10, pady=(5,0))
        self.log_area = scrolledtext.ScrolledText(self.root, wrap=tk.WORD, font=("Consolas", 9))
        self.log_area.grid(row=6, column=0, sticky="nsew", padx=10, pady=(0,10))

        self.info_label = tk.Label(self.root, font=("Arial", 8), fg="grey")
        self.info_label.grid(row=7, column=0, sticky="ew", padx=10, pady=5)

    def update_undo_button_state(self):
        selected_dir = self.directory_path_var.get()
        undo_log_path = ""
        if selected_dir and os.path.isdir(selected_dir):
            undo_log_path = os.path.join(selected_dir, UNDO_LOG_FILE_NAME)

        if os.path.exists(undo_log_path):
            self.undo_button.config(state=tk.NORMAL)
        else:
            self.undo_button.config(state=tk.DISABLED)


    def open_selected_folder(self):
        folder_path = self.directory_path_var.get()
        if folder_path and os.path.isdir(folder_path):
            try:
                if sys.platform == "win32": os.startfile(folder_path)
                elif sys.platform == "darwin": subprocess.Popen(["open", folder_path])
                else: subprocess.Popen(["xdg-open", folder_path])
            except Exception as e: messagebox.showerror("Error", f"Could not open folder: {e}")
        else: messagebox.showwarning("Warning", "No folder selected or folder does not exist.")


    def open_user_categories_dialog(self):
        dialog = UserCategoriesDialog(self.root,
                                      title=self.strings.get("user_categories_title", "User Categories"),
                                      app_strings=self.strings,
                                      current_user_categories_list=self.user_defined_categories, # Передаем копию
                                      current_default_category_configs_dict=self.default_category_configs, # Передаем копию
                                      all_default_category_internal_keys_list=ALL_DEFAULT_CATEGORY_INTERNAL_KEYS,
                                      original_default_extensions_map=DEFAULT_CATEGORY_EXTENSIONS_MAP,
                                      original_default_folder_names_map=LANGUAGES[self.current_lang_code]["default_folder_names_on_disk"],
                                      original_java_subfolder_names_map=LANGUAGES[self.current_lang_code]["java_subfolder_names_on_disk"]
                                      )

        if dialog.result is not None:
            self.user_defined_categories, self.default_category_configs = dialog.result
            self._populate_categories_checkboxes()
            self.auto_save_configuration()


    def _populate_categories_checkboxes(self):
        for widget in self.categories_inner_frame.winfo_children(): widget.destroy()

        num_columns = 3
        for i in range(num_columns):
            self.categories_inner_frame.columnconfigure(i, weight=1)

        current_row = 0; current_col = 0
        
        temp_active_vars_snapshot = {} # Для сохранения состояний галочек

        # Стандартные категории
        for internal_key in ALL_DEFAULT_CATEGORY_INTERNAL_KEYS:
            config = self.default_category_configs.get(internal_key, {})
            # Имя папки на диске (может быть изменено пользователем)
            folder_name_on_disk = config.get('folder_name_on_disk', 
                                             LANGUAGES[self.current_lang_code]["default_folder_names_on_disk"].get(internal_key, internal_key))
            # "Оригинальное" UI имя категории для текущего языка (неизменяемое пользователем напрямую в этом поле)
            original_ui_name = self.strings["categories_internal_keys_display_names"].get(internal_key, internal_key)
            
            display_text_for_checkbox = folder_name_on_disk
            if folder_name_on_disk != original_ui_name:
                 display_text_for_checkbox = f"{folder_name_on_disk} ({original_ui_name})"

            var = self.active_categories_vars.get(internal_key, tk.BooleanVar(value=True))
            temp_active_vars_snapshot[internal_key] = var

            cb = ttk.Checkbutton(self.categories_inner_frame, text=display_text_for_checkbox, variable=var, command=self.auto_save_configuration)
            cb.grid(row=current_row, column=current_col, sticky='w', padx=5, pady=2)
            current_col += 1
            if current_col >= num_columns: current_col = 0; current_row += 1

        # Пользовательские категории
        for user_cat in self.user_defined_categories:
            cat_id = user_cat.get('id')
            if not cat_id: continue

            display_text = user_cat.get('folder_name_on_disk', 'User Category')
            
            var = self.active_categories_vars.get(cat_id, tk.BooleanVar(value=True))
            temp_active_vars_snapshot[cat_id] = var

            cb = ttk.Checkbutton(self.categories_inner_frame, text=f"[U] {display_text}", variable=var, command=self.auto_save_configuration)
            cb.grid(row=current_row, column=current_col, sticky='w', padx=5, pady=2)
            current_col += 1
            if current_col >= num_columns: current_col = 0; current_row += 1
        
        self.active_categories_vars = temp_active_vars_snapshot


    def update_ui_language(self):
        self.strings = LANGUAGES[self.current_lang_code]
        self.root.title(self.strings["title"])

        lang_options_display_map = {"ru": "Русский", "en": "English"}
        self.selected_language_var.set(lang_options_display_map.get(self.current_lang_code, "English"))


        self.lang_label.config(text=self.strings["language_label"])
        self.settings_label_widget.config(text=self.strings["program_settings_label"])

        self.customize_cat_btn.config(text=self.strings["customize_categories_button"])
        self.open_folder_btn.config(text=self.strings["open_folder_button"])
        self.undo_button.config(text=self.strings["undo_last_sort_button"])


        self.path_label.config(text=self.strings["browse_folder_label"])
        self.browse_button.config(text=self.strings["browse_button"])
        self.categories_outer_frame.config(text=self.strings["categories_label"])
        
        self._populate_categories_checkboxes()

        self.select_all_btn.config(text=self.strings["select_all_button"])
        self.deselect_all_btn.config(text=self.strings["deselect_all_button"])
        self.options_frame.config(text=self.strings["options_label"])
        self.dry_run_cb.config(text=self.strings["dry_run_checkbox"])
        self.organize_by_date_cb.config(text=self.strings["organize_by_date_checkbox"])
        self.conflict_label_widget.config(text=self.strings["conflict_label"])

        conflict_options_map_code_to_display = {
            "rename": self.strings["conflict_rename"],
            "skip": self.strings["conflict_skip"]
        }
        self.conflict_combobox.config(values=list(conflict_options_map_code_to_display.values()))
        
        current_conflict_code = self.conflict_resolution_var.get()
        if not current_conflict_code or current_conflict_code not in conflict_options_map_code_to_display:
            current_conflict_code = "rename"
            self.conflict_resolution_var.set(current_conflict_code)
        
        self.conflict_combobox.set(conflict_options_map_code_to_display[current_conflict_code])

        self.start_button.config(text=self.strings["start_button_idle"])
        self.log_label_widget.config(text=self.strings["log_label"])
        self.info_label.config(text=self.strings["info_label_template"])

    def change_language_and_autosave(self, event=None):
        selected_display_name = self.selected_language_var.get()
        lang_options_reverse = {"Русский": "ru", "English": "en"}
        new_lang_code = lang_options_reverse.get(selected_display_name)
        
        if new_lang_code and new_lang_code != self.current_lang_code:
            old_lang_code = self.current_lang_code
            self.current_lang_code = new_lang_code
            self.strings = LANGUAGES[self.current_lang_code]
            
            saved_customizations = {
                key: {
                    'folder_name_on_disk': self.default_category_configs[key]['folder_name_on_disk'],
                    'extensions': list(self.default_category_configs[key]['extensions']),
                    'subfolder_names_on_disk': dict(self.default_category_configs[key].get('subfolder_names_on_disk', {})) if key == JAVA_INTERNAL_KEY else None
                } for key in ALL_DEFAULT_CATEGORY_INTERNAL_KEYS if key in self.default_category_configs
            }

            self._initialize_default_category_configs(new_lang_code)

            for key, custom_data in saved_customizations.items():
                old_lang_default_folder_name = LANGUAGES[old_lang_code]["default_folder_names_on_disk"].get(key, key)
                if custom_data['folder_name_on_disk'] != old_lang_default_folder_name:
                    self.default_category_configs[key]['folder_name_on_disk'] = custom_data['folder_name_on_disk']
                
                self.default_category_configs[key]['extensions'] = custom_data['extensions']

                if key == JAVA_INTERNAL_KEY and custom_data['subfolder_names_on_disk'] is not None:
                    old_lang_java_subfolders = LANGUAGES[old_lang_code]["java_subfolder_names_on_disk"]
                    current_java_subfolders_config = self.default_category_configs[key]['subfolder_names_on_disk']
                    
                    for sub_key, saved_sub_name in custom_data['subfolder_names_on_disk'].items():
                        if saved_sub_name != old_lang_java_subfolders.get(sub_key, sub_key):
                             current_java_subfolders_config[sub_key] = saved_sub_name

            self.update_ui_language()
            self.auto_save_configuration()


    def load_configuration(self, silent=False):
        config_path = os.path.join(self.script_dir, CONFIG_FILE_NAME)
        initial_lang_code_before_load = self.current_lang_code

        if not os.path.exists(config_path):
            if not silent:
                messagebox.showwarning(self.strings.get("settings_load_error_title", "Config Error"),
                                   self.strings.get("settings_file_not_found", f"Settings file not found: {{filepath}}").format(filepath=config_path))
            self.strings = LANGUAGES[initial_lang_code_before_load]
            self._initialize_default_category_configs(initial_lang_code_before_load)
            self.update_ui_language()
            self.update_undo_button_state()
            return

        config = configparser.ConfigParser()
        try:
            config.read(config_path, encoding='utf-8')
            
            loaded_lang_code = initial_lang_code_before_load
            if config.has_section('Settings'):
                settings_data = config['Settings']
                raw_lang_from_ini = settings_data.get('language', initial_lang_code_before_load)
                prospective_lang_code = str(raw_lang_from_ini if raw_lang_from_ini is not None else initial_lang_code_before_load)
                if prospective_lang_code in LANGUAGES:
                    loaded_lang_code = prospective_lang_code
                else:
                    print(f"Warning: Loaded invalid language code '{prospective_lang_code}'. Falling back to '{initial_lang_code_before_load}'.")
            
            self.current_lang_code = loaded_lang_code
            self.strings = LANGUAGES[self.current_lang_code]

            self._initialize_default_category_configs(self.current_lang_code)

            if config.has_section('Settings'):
                settings_data = config['Settings']
                self.directory_path_var.set(str(settings_data.get('target_directory', '')))
                self.dry_run_var.set(settings_data.getboolean('dry_run', False))
                self.organize_by_date_var.set(settings_data.getboolean('organize_by_date', False))
                self.conflict_resolution_var.set(str(settings_data.get('conflict_resolution', 'rename')))
            
            if config.has_section('UserDefinedCategories') and config.has_option('UserDefinedCategories', 'categories_json'):
                try: self.user_defined_categories = json.loads(config.get('UserDefinedCategories','categories_json'))
                except json.JSONDecodeError: self.user_defined_categories = []; print("Error UserDefinedCategories JSON")
            else: self.user_defined_categories = []

            if config.has_section('DefaultCategoryConfigs') and config.has_option('DefaultCategoryConfigs', 'configs_json'):
                try:
                    loaded_default_configs_customizations = json.loads(config.get('DefaultCategoryConfigs','configs_json'))
                    for key, custom_data in loaded_default_configs_customizations.items():
                        if key in self.default_category_configs: 
                            if 'folder_name_on_disk' in custom_data and isinstance(custom_data['folder_name_on_disk'], str):
                                self.default_category_configs[key]['folder_name_on_disk'] = custom_data['folder_name_on_disk']
                            if 'extensions' in custom_data and isinstance(custom_data['extensions'], list):
                                self.default_category_configs[key]['extensions'] = custom_data['extensions']
                            if 'subfolder_names_on_disk' in custom_data and key == JAVA_INTERNAL_KEY and isinstance(custom_data['subfolder_names_on_disk'], dict):
                                self.default_category_configs[key]['subfolder_names_on_disk'] = custom_data['subfolder_names_on_disk']
                except json.JSONDecodeError: print("Error DefaultCategoryConfigs JSON")

            self.active_categories_vars.clear() 
            all_cat_keys_for_checkboxes = list(self.default_category_configs.keys()) + [uc.get('id') for uc in self.user_defined_categories if uc.get('id')]
            
            if config.has_section('ActiveCategoriesState') and config.has_option('ActiveCategoriesState', 'states_json'):
                try:
                    loaded_active_vars_states = json.loads(config.get('ActiveCategoriesState','states_json'))
                    for cat_key_or_id in all_cat_keys_for_checkboxes:
                        self.active_categories_vars[cat_key_or_id] = tk.BooleanVar(value=loaded_active_vars_states.get(cat_key_or_id, True))
                except json.JSONDecodeError:
                     print("Error ActiveCategoriesState JSON")
                     for cat_key_or_id in all_cat_keys_for_checkboxes:
                         self.active_categories_vars[cat_key_or_id] = tk.BooleanVar(value=True)
            else:
                for cat_key_or_id in all_cat_keys_for_checkboxes:
                    self.active_categories_vars[cat_key_or_id] = tk.BooleanVar(value=True)
            
            self.update_ui_language() 

            if not silent:
                messagebox.showinfo(self.strings["settings_loaded_title"], self.strings["settings_loaded_message"].format(filepath=config_path))
            
            self.open_folder_btn.config(state=tk.NORMAL if self.directory_path_var.get() else tk.DISABLED)
            self.update_undo_button_state()

            if self.directory_path_var.get():
                 log_message(self.log_area, None, self.strings, "log_folder_selected", folder=self.directory_path_var.get())
        
        except Exception as e:
            if not silent: 
                messagebox.showerror(self.strings.get("settings_load_error_title", "Error Loading Settings"), 
                                     self.strings.get("settings_load_error_message", "Failed to load: {error}").format(filepath=config_path, error=e))
            else: 
                print(f"Error loading configuration silently: {e}") 
            
            self.current_lang_code = initial_lang_code_before_load
            self.strings = LANGUAGES[self.current_lang_code]
            self._initialize_default_category_configs(self.current_lang_code)
            self.user_defined_categories = [] 
            self.active_categories_vars.clear() 
            for key in ALL_DEFAULT_CATEGORY_INTERNAL_KEYS: 
                self.active_categories_vars[key] = tk.BooleanVar(value=True)
            
            self.update_ui_language() 
            self.update_undo_button_state()


    def select_all_categories_and_autosave(self):
        for var in self.active_categories_vars.values(): var.set(True)
        self.auto_save_configuration()

    def deselect_all_categories_and_autosave(self):
        for var in self.active_categories_vars.values(): var.set(False)
        self.auto_save_configuration()

    def browse_directory_and_autosave(self):
        initial_dir = self.directory_path_var.get() or os.path.expanduser("~")
        dialog_title = self.strings.get("browse_dialog_title", "Select Folder")
        directory = filedialog.askdirectory(initialdir=initial_dir, title=dialog_title)
        if directory:
            self.directory_path_var.set(directory)
            self.log_area.delete('1.0', tk.END)
            log_message(self.log_area, None, self.strings, "log_folder_selected", folder=directory)
            self.open_folder_btn.config(state=tk.NORMAL)
            self.update_undo_button_state()
            self.auto_save_configuration()
            

    def start_organization_thread(self):
        selected_directory = self.directory_path_var.get()
        if not selected_directory:
            messagebox.showerror(self.strings["error_no_folder_selected_title"], self.strings["error_no_folder_selected_message"]); return

        try:
            norm_script_dir = os.path.normpath(self.script_dir)
            norm_selected_dir = os.path.normpath(selected_directory)
            if norm_selected_dir == norm_script_dir or norm_script_dir.startswith(norm_selected_dir + os.sep):
                messagebox.showerror(self.strings["error_sorting_program_folder_title"], self.strings["error_sorting_program_folder_message"]); return
        except Exception as e: print(f"Ошибка при проверке пути к скрипту: {e}")

        warning_msg = self.strings["warning_pre_sort_message"].format(folder=selected_directory)
        if not messagebox.askyesno(self.strings["warning_pre_sort_title"], warning_msg): return

        active_categories_config_map = {key_or_id: var.get() for key_or_id, var in self.active_categories_vars.items()}
        dry_run_active = self.dry_run_var.get()
        organize_by_date_active = self.organize_by_date_var.get()

        conflict_display_name = self.conflict_combobox.get()
        actual_conflict_resolution = "rename"
        if conflict_display_name == self.strings["conflict_skip"]: actual_conflict_resolution = "skip"

        self.log_area.delete('1.0', tk.END)
        self.start_button.config(state=tk.DISABLED, text=self.strings["start_button_busy"])
        self.browse_button.config(state=tk.DISABLED)

        self.customize_cat_btn.config(state=tk.DISABLED)
        self.open_folder_btn.config(state=tk.DISABLED)
        self.undo_button.config(state=tk.DISABLED)


        thread = threading.Thread(target=self._run_organization_and_reactivate_buttons,
                                  args=(selected_directory, active_categories_config_map,
                                        [dict(cat) for cat in self.user_defined_categories],
                                        {k: dict(v) for k, v in self.default_category_configs.items()},
                                        self.log_area, self.strings,
                                        dry_run_active, organize_by_date_active, actual_conflict_resolution))
        thread.daemon = True
        thread.start()

    def _run_organization_and_reactivate_buttons(self, directory, active_config_map_for_thread,
                                                 user_cats_for_thread, default_configs_for_thread,
                                                 log_widget, current_strings_for_thread,
                                                 dry_run, organize_by_date, conflict_resolution):
        moved_summary = {}
        undo_log = []
        try:
            moved_summary, undo_log = organize_files(directory, active_config_map_for_thread,
                                           user_cats_for_thread, default_configs_for_thread,
                                           log_widget, current_strings_for_thread,
                                           dry_run, organize_by_date, conflict_resolution)
        except Exception as e:
            if log_widget and log_widget.winfo_exists():
                log_message(log_widget, None, current_strings_for_thread, "error_critical_message_template", error=e)
                messagebox.showerror(current_strings_for_thread.get("error_critical_title", "Critical Error"),
                                     current_strings_for_thread.get("error_critical_message_template","Unexpected error: {error}").format(error=e))
            else: print(f"Критическая ошибка в потоке сортировки (логгер недоступен): {e}")
        finally:
            self.root.after(0, lambda: self._reactivate_buttons(moved_summary, dry_run, undo_log))

    def _reactivate_buttons(self, moved_summary=None, dry_run=False, undo_log_operations=None):
        try:
            if self.start_button.winfo_exists(): self.start_button.config(state=tk.NORMAL, text=self.strings["start_button_idle"])
            if self.browse_button.winfo_exists(): self.browse_button.config(state=tk.NORMAL)

            if self.customize_cat_btn.winfo_exists(): self.customize_cat_btn.config(state=tk.NORMAL)
            if self.open_folder_btn.winfo_exists(): self.open_folder_btn.config(state=tk.NORMAL if self.directory_path_var.get() else tk.DISABLED)
            self.update_undo_button_state()


            if not dry_run and moved_summary:
                if not any(moved_summary.values()):
                     log_message(self.log_area, None, self.strings, "log_summary_no_files_moved")
                else:
                    for cat_folder_name, count in moved_summary.items():
                        if count > 0:
                             log_message(self.log_area, None, self.strings, "log_summary_moved_to", category_folder_name=cat_folder_name, count=count)

        except tk.TclError: pass

    def start_undo_thread(self):
        selected_dir = self.directory_path_var.get()
        if not selected_dir: return

        undo_log_path = os.path.join(selected_dir, UNDO_LOG_FILE_NAME)
        if not os.path.exists(undo_log_path):
            messagebox.showinfo(self.strings["undo_no_log_title"],
                                self.strings["undo_no_log_message"].format(folder=selected_dir))
            self.update_undo_button_state()
            return

        confirm_msg = self.strings["undo_confirm_message"].format(folder=selected_dir)
        if not messagebox.askyesno(self.strings["undo_confirm_title"], confirm_msg):
            return

        self.start_button.config(state=tk.DISABLED)
        self.browse_button.config(state=tk.DISABLED)
        self.customize_cat_btn.config(state=tk.DISABLED)
        self.open_folder_btn.config(state=tk.DISABLED)
        self.undo_button.config(state=tk.DISABLED, text=self.strings.get("start_button_busy", "Working..."))


        thread = threading.Thread(target=self._execute_undo, args=(selected_dir, undo_log_path, self.log_area, self.strings))
        thread.daemon = True
        thread.start()

    def _execute_undo(self, target_dir, log_path, log_widget, current_strings_for_thread):
        logger_with_strings = lambda msg_key, **kwargs: log_message(log_widget, None, current_strings_for_thread, msg_key, **kwargs)
        logger_with_strings("undo_starting", folder=target_dir)
        restored_count = 0
        failed_count = 0

        try:
            with open(log_path, 'r', encoding='utf-8') as f:
                log_data = json.load(f)

            operations = log_data.get("operations", [])
            for op in reversed(operations):
                source_to_restore_to = op.get('source_abs')
                current_location = op.get('dest_abs')

                if not source_to_restore_to or not current_location: continue

                original_filename = os.path.basename(source_to_restore_to)

                if os.path.exists(source_to_restore_to):
                    logger_with_strings("undo_file_conflict_at_original", original_path=source_to_restore_to, filename=original_filename)
                    failed_count +=1
                    continue

                try:
                    original_parent_dir = os.path.dirname(source_to_restore_to)
                    if not os.path.exists(original_parent_dir):
                        os.makedirs(original_parent_dir, exist_ok=True)

                    shutil.move(current_location, source_to_restore_to)
                    logger_with_strings("undo_file_restored", filename=original_filename, original_path=source_to_restore_to)
                    restored_count +=1
                except Exception as e:
                    logger_with_strings("undo_file_restore_failed", filename=original_filename, original_path=source_to_restore_to, error=e)
                    failed_count +=1

            if restored_count > 0: logger_with_strings("undo_summary_restored", count=restored_count)
            if failed_count > 0: logger_with_strings("undo_summary_failed", count=failed_count)

            os.remove(log_path)
            logger_with_strings("undo_complete")

        except Exception as e:
            logger_with_strings("undo_error_reading_log", error=e)
        finally:
            self.root.after(0, self._reactivate_buttons_after_undo)

    def _reactivate_buttons_after_undo(self):
        self._reactivate_buttons()
        self.update_undo_button_state()


if __name__ == "__main__":
    root = tk.Tk()
    app = FileOrganizerApp(root)
    root.mainloop()
