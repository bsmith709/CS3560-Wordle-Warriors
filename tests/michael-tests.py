import unittest

class unitTests(unittest.TestCase):
    # Test to check if the display time is decremented by 1
    def test_text_display_time(self):
        display_time = 120
        time_after = notValidWordText(display_time)
        self.assertEqual(time_after, display_time - 1)
    # Test to check if the display time is not decremented when it is 0
    def test_text_display_time_zero(self):
        display_time = 0
        time_after = notValidWordText(display_time)
        self.assertEqual(time_after, display_time)
    # Test to check if the display time is not decremented when it is negative
    def test_text_display_time_negative(self):
        display_time = -1
        time_after = notValidWordText(display_time)
        self.assertEqual(time_after, display_time)

def notValidWordText(text_display_time):
    if(text_display_time > 0):
        #font = pygame.font.Font(None, 36)
        #text_not_real_word = font.render("Please only enter valid words!", True, 'white')
        #screen.blit(text_not_real_word, (SCREEN_WIDTH // 2 - 177, SCREEN_HEIGHT // 2 - 328))
        text_display_time -= 1
    return text_display_time

if __name__ == '__main__':
    unittest.main()