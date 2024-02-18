import os


def get_file_name(file_path: str) -> str:
    return os.path.splitext(os.path.basename(file_path))[0]


def list_to_str(values: list[str]) -> str:
    result = ", ".join(values)

    last_comma_index = result.rfind(",")
    if last_comma_index != -1:
        result = (
            result[:last_comma_index] + " and" + result[last_comma_index + 1 :]
        )

    return result
