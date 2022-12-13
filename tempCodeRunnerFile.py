#Chỗ này thay bằng if <ẤN VÀO NÚT NEW GAME>#
                if start_button.rect.collidepoint(x, y):
                    if (x >= 70 and x <= 350 and y >= 330 and y <= 430):
                #âm thanh new game (xem ztype)
                        runGame()

                #thêm dòng if ấn vào nút QUIT thì pygame.quit()
                if exit_button.rect.collidepoint(x, y):
                    if (x >= 121 and x <= 305 and y >= 466 and y <= 530):
                        main_running = False