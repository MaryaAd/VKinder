from vk_api.keyboard import VkKeyboard, VkKeyboardColor

start_keyboard = VkKeyboard(inline=True)
start_keyboard.add_button('Привет', VkKeyboardColor.PRIMARY)
main_keyboard = VkKeyboard(inline=True)
main_keyboard.add_button('Да', VkKeyboardColor.PRIMARY)
main_keyboard.add_button('Нет', VkKeyboardColor.PRIMARY)
find_keyboard = VkKeyboard(inline=True)
find_keyboard.add_button('Добавить', VkKeyboardColor.PRIMARY)
find_keyboard.add_button('Заблокировать', VkKeyboardColor.PRIMARY)
find_keyboard.add_button('Далее', VkKeyboardColor.PRIMARY)
find_keyboard.add_button('Выход', VkKeyboardColor.PRIMARY)
next_keyboard = VkKeyboard(inline=True)
next_keyboard.add_button('1', VkKeyboardColor.PRIMARY)
next_keyboard.add_button('0', VkKeyboardColor.PRIMARY)
