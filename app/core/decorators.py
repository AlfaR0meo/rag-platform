import time
from functools import wraps
from app.core.logger import logger

# Декоратор для логирования выполнения функций
def log_execution(action: str):
    def decorator(func):
        # Используем wraps для сохранения метаданных оригинальной функции
        @wraps(func)
        # Внутренняя функция-обертка для логирования
        def wrapper(*args, **kwargs):

            print("DECORATOR WORKS")

            # Засекаем время начала выполнения функции
            start_time = time.time()

            # Логируем начало выполнения функции с указанием действия и имени функции (без @wraps будет отображаться имя wrapper, а не оригинальной функции)
            logger.info(
                "function_started",
                action=action,
                function=func.__name__,
            )

            # Пытаемся выполнить оригинальную функцию и логируем результат
            try:
                # Получаем результат выполнения функции
                result = func(*args, **kwargs)

                # Засекаем время окончания выполнения функции и вычисляем общее время выполнения
                execution_time = time.time() - start_time
                
                # Логируем успешное завершение функции с указанием действия, имени функции и времени выполнения
                logger.info(
                    "function_completed",
                    action=action,
                    function=func.__name__,
                    execution_time=round(execution_time, 4),
                )
                # Возвращаем результат выполнения функции
                return result
            # Логируем любые исключения, возникшие при выполнении функции, с указанием действия, имени функции и текста ошибки, а затем повторно выбрасываем исключение для дальнейшей обработки
            except Exception as e:
                logger.error(
                    "function_failed",
                    action=action,
                    function=func.__name__,
                    error=str(e),
                )
                raise
        # Возвращаем обертку, которая будет использоваться вместо оригинальной функции
        return wrapper
    # Возвращаем декоратор, который можно применять к функциям для логирования их выполнения
    return decorator

# Асинхронный декоратор для логирования выполнения асинхронных функций
def async_log_execution(action: str):
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):

            start_time = time.time()

            logger.info(
                "function_started",
                action=action,
                function=func.__name__,
            )

            try:
                result = await func(*args, **kwargs)

                execution_time = time.time() - start_time

                logger.info(
                    "function_completed",
                    action=action,
                    function=func.__name__,
                    execution_time=round(execution_time,4),
                )

                return result
            except Exception as e:
                logger.error(
                    "function_failed",
                    action=action,
                    function=func.__name__,
                    error=str(e),
                )
                raise
        return wrapper
    return decorator
