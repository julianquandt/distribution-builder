import pygame, csv, math, os, numpy

scrInfo = pygame.display.Info()
#rgb-colors
black = (0,0,0)
white = (255,255,255)
green = (0,96,27)
red = (225,0,25)

this_folder = os.path.abspath(os.path.dirname(__file__))
continue_file = os.path.join(this_folder, 'packageData//continue.png')
continue_mouseover_file = os.path.join(this_folder, 'packageData//continue_mouseover.png')


def quitExp():
    quitDlg = gui.Dlg(title="Quit Experiment?")
    quitDlg.addText("Quit Experiment?")
    quitDlg.show()  # show dialog and wait for OK or Cancel
    if quitDlg.OK:
        pygame.quit()
        sys.exit()
    else:
       pass


def drawStaticTicks(Screen, scale_numbers, tick_positions, tick_font, offset = 20, tick_mode = "static", precision = 1 , custom_ticks = ["", ""]):
    # drawing the tick-marks under the scale
    if tick_mode == "static":
        for i in range(0, len(scale_numbers)): # draw each tickmark and their position from the provided list

            temp_font = tick_font.render(str(scale_numbers[i]), True, (0, 0, 0))
            if i%2 == 0: #if index is even
                Screen.blit(temp_font, tick_positions[i])
            else:
                Screen.blit(temp_font, (tick_positions[i][0], tick_positions[i][1] + offset))
    elif tick_mode == "custom":
        pos_divide = int(math.floor(len(tick_positions)/(len(custom_ticks)-1)))
        temp_font = tick_font.render(str(custom_ticks[0]), True, (0, 0, 0))
        Screen.blit(temp_font, tick_positions[0])
        for i in range(1, len(custom_ticks)):  # draw each tickmark and their position from the provided list of custom ticks
            temp_font = tick_font.render(str(custom_ticks[i]), True, (0, 0, 0))
            if (len(tick_positions)-(len(custom_ticks)-(i+1))*pos_divide) == len(tick_positions):
                Screen.blit(temp_font, (tick_positions[(len(tick_positions)-(len(custom_ticks)-(i+1))*pos_divide)-1][0]-temp_font.get_rect().size[0],
                                        tick_positions[(len(tick_positions) - (len(custom_ticks) - (i + 1)) * pos_divide) - 1][1]))
            else:
                Screen.blit(temp_font, (tick_positions[(len(tick_positions)-(len(custom_ticks)-(i+1))*pos_divide)-1][0]-temp_font.get_rect().size[0]/2,
                                        tick_positions[(len(tick_positions) - (len(custom_ticks) - (i + 1)) * pos_divide) - 1][1]))
    else:
        for i in range(0, len(scale_numbers)):  # draw each tickmark and their position from the provided list
            if i % (10/precision) == 0:
                temp_font = tick_font.render(str(scale_numbers[i]), True, (0, 0, 0))
                Screen.blit(temp_font, (tick_positions[i][0], tick_positions[i][1] + offset * 2))


def drawFloatingTick(Screen, scale_numbers, tick_positions, tick_position, tick_font):

    tick_font.set_bold(True)
    floating_mark = tick_font.render(str(scale_numbers[tick_positions.index(tick_position)]), True, (0, 0, 0))
    Screen.blit(floating_mark, (tick_position[0], tick_position[1]))
    tick_font.set_bold(False)


def drawBars(df_name, pp_info, Screen, line_y_init, tick_positions, points,
             line_x_end, height_list, remaining_points, continue_img,
             continue_mouseover_img, timer, min, precision, scale_numbers,
             tick_font, tick_mode = "floating", max_height = 0.99, **kwargs):
    # drawing the bars
    if len(kwargs) > 0:
        added_vars = kwargs
    grid_y_max = line_y_init - line_y_init * max_height # the maximum height of a bar
    box_y_size = abs(int((grid_y_max - line_y_init)/points)) # scale the height of each point to the maximum bar height
    if pygame.mouse.get_pos()[0] in range(tick_positions[0][0], tick_positions[len(tick_positions) - 1][0]): # if mouse is within rating-scale range

        for i in tick_positions[:-1]: # check each tick-position

            # if tick_positions.index(i) == len(tick_positions)-1: # if at the end of the scale the bar ends at the line end
            #     bar_x_end = line_x_end-17
            # else:
            bar_x_end = tick_positions[tick_positions.index(i) + 1][0] # otherwise its ends at the next interval
            bar_i_height = line_y_init - height_list[tick_positions.index(i)] # calculate bar height
            Screen.fill(black, [i[0], bar_i_height, bar_x_end-i[0], line_y_init-bar_i_height]) # draw bar


            if remaining_points == 0: # show continue button if points are all used
                button = displayContinue(Screen, continue_img, continue_mouseover_img)

            if pygame.mouse.get_pos()[0] in range(int(i[0]), int(bar_x_end)): # if mouse is at any bars x-positions
                if tick_mode == "floating":
                    drawFloatingTick(Screen, scale_numbers, tick_positions, i, tick_font)

                bar_y_init = line_y_init - height_list[tick_positions.index(i)] - box_y_size
                bar_y_init_draw = bar_y_init# position where potential addition / substraction should be situated
                if pygame.mouse.get_pos()[1] < bar_y_init+box_y_size: # get mouse position to see whether its an addition or substraction
                    col = green # draw green if its an addition
                else:
                    col = red # draw red if its an deletion
                    if height_list[tick_positions.index(i)] > 0: # do not draw beneath line if bar height = 0
                        bar_y_init_draw = bar_y_init+box_y_size
                Screen.fill(col, [i[0], bar_y_init_draw, bar_x_end-i[0], box_y_size])

                for event in pygame.event.get(): # check whether an event occured

                        #ask whether experiment should be quit when ESCAPE is pressed
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_ESCAPE:
                            quitExp()

                    if event.type == pygame.MOUSEBUTTONDOWN:

                        if remaining_points == 0: # if remaining points are 0 and button is pressed and its in the continue button, next trial
                            if button.collidepoint(pygame.mouse.get_pos()) and event.button == 1:
                                saveDistributionData(df_name, pp_info, height_list, remaining_points, "increase",
                                                     pygame.time.get_ticks() - timer, box_y_size,
                                                     min, precision, points, summary = True, **kwargs)
                                return (height_list, remaining_points, True, True)

                        if pygame.mouse.get_pos()[1] < bar_y_init + box_y_size and event.button in [1,4]: # if not, it might be a bar increase
                            if remaining_points > 0:
                                height_list[tick_positions.index(i)] += box_y_size
                                remaining_points -= 1
                                saveDistributionData(df_name, pp_info, height_list, remaining_points, "increase",
                                                     pygame.time.get_ticks()-timer, box_y_size,
                                                     min, precision, points, summary = False, **kwargs)

                        elif event.button in [1,5]:
                            if height_list[tick_positions.index(i)] > 0: # or decrease
                                height_list[tick_positions.index(i)] -= box_y_size
                                remaining_points += 1
                                saveDistributionData(df_name, pp_info, height_list, remaining_points, "decrease",
                                                     pygame.time.get_ticks()-timer, box_y_size,
                                                     min, precision, points, summary = False, **kwargs)

                        return(height_list, remaining_points, False, True)
                            # return current bar-list and whether trial is finished and whether timer should be reset

    else: #TODO: fix this more elegantly, now it is only preventing the program from crashing when mousepos leaves scale boundaries
        for event in pygame.event.get():  # check whether an event occured
            # ask whether experiment should be quit when ESCAPE is pressed
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    quitExp()

    return(height_list, remaining_points, False, False)
    # return current bar-list and whether trial is finished without resetting timer as no action was taken


def displayPoints(Screen, line_x_init, line_y_init, remaining_points, pointFont):
    # displaying remaining points

    point_text = "Remaining Points = " + str(remaining_points)
    point_display = pointFont.render(point_text, True, (0, 0, 0))
    point_width = pointFont.size(point_text)[0]
    Screen.blit(point_display, (line_x_init - 0.5 * point_width, line_y_init + 0.1 * scrInfo.current_h))


def displayContinue(Screen, continue_img, continue_mouseover_img):
    # display continue button if remaining points are 0

    button = Screen.blit(continue_img, (int(scrInfo.current_w-450), int(scrInfo.current_h-150)))  # draw button

    if button.collidepoint(pygame.mouse.get_pos()):
        button = Screen.blit(continue_mouseover_img, (int(scrInfo.current_w - 450), int(scrInfo.current_h-150)))  # draw button

    return button


def bin2value(height_list, box_y_size, min, precision):
    #transform the bin-value (i.e. number of the n-th bar to its value in terms of the scale)

    freq_list = [i/box_y_size for i in height_list]
    val_list = [min+i*precision+(precision/2) for i in range(0, len(height_list))]
    dist_array = []
    for i in range(0, len(height_list)):

        if freq_list[i] > 0:
            for k in range (0, int(freq_list[i])):
                dist_array.append(val_list[i])


    return freq_list, dist_array


def saveDistributionData(df_name, pp_info, height_list, remaining_points, action, rt, box_y_size, min, precision, points, summary = False, **kwargs):
    #save distribution data (after each increase / decrease)
    if summary:
        df_name = df_name[:-4]+"_summary.csv"
    if len(kwargs) > 0:
        added_vars = kwargs
    else:
        added_vars = None
    #print([added_vars['added_vars'][i][0] for i in range(len(added_vars['added_vars']))])
    if not os.path.isfile(df_name):
        with open(df_name, "a") as dbf:
            wr = csv.writer(dbf, delimiter=',', lineterminator='\r')
            vl_var_names = ['bin_'+str(i) for i in range(1, len(height_list)+1)]
            vl_point_names = ['point_'+str(i) for i in range(1, points+1)]
            row_names = ['ppid', 'remaining_points', 'action', 'rt', 'box_y_size', 'mean', 'sd']+vl_var_names+vl_point_names
            if added_vars:
                row_names = row_names + [added_vars['added_vars'][i][0] for i in range(len(added_vars['added_vars']))]
            wr.writerow(row_names)

    freq_list, dist_array = bin2value(height_list, box_y_size, min, precision)
    dist_m = numpy.mean(dist_array)
    dist_sd = numpy.std(dist_array)
    empty_dist_array = [None for i in range(remaining_points)]
    new_vars = [pp_info['subjectID'], remaining_points, action, rt, box_y_size, dist_m, dist_sd]
    row = new_vars + freq_list+dist_array+empty_dist_array
    if added_vars:
        row = row + [added_vars['added_vars'][i][1] for i in range(len(added_vars['added_vars']))]
    with open(df_name, "a") as dbf:
        wr = csv.writer(dbf, delimiter=',',lineterminator='\r')
        wr.writerow(row)


def distributionBuilder(df_name, pp_info, Screen, stim, min=0, max=250, scale_length=0.8, precision=100, points=50,
                        pos=(0, 0), offset=20, tick_mode = "floating", max_height = 0.99, custom_ticks = ["", ""], **kwargs):
    # running a single distribution builder trial (i.e. until 1 stimulus is rated)
    if len(kwargs)>0:
        added_vars = kwargs
    else:
        added_vars = 0
    continue_img = pygame.image.load(continue_file).convert_alpha()  # load the continue-button image
    continue_mouseover_img = pygame.image.load(continue_mouseover_file).convert_alpha()

    stim_img = pygame.image.load(stim).convert_alpha()
    stim_img = pygame.transform.scale(stim_img, (300,int(stim_img.get_rect().size[1] * (300.0 / stim_img.get_rect().size[0]))))

    # initiate the position of the lines start and end-point (relative to screen center)
    line_x_init = int(scrInfo.current_w*0.5)+int(pos[0])
    line_y_init = int(scrInfo.current_h*0.8)+int(pos[0])
    line_x_start = line_x_init-int(scrInfo.current_w * 0.5 * scale_length)
    line_y_start = line_y_init
    line_x_end = line_x_init+int(scrInfo.current_w * 0.5 * scale_length)
    line_y_end = line_y_start

    # tick-mark font and point-font
    tick_font = pygame.font.SysFont('Arial', 25)
    point_font = pygame.font.SysFont('Arial', 50, bold = True)

    scale_numbers = [i for i in range(min, max+1, precision)] # a list of the scale-numbers to be displayed as ticks

    # make a list of tickmark-positions
    tick_positions = [(line_x_start,line_y_start)]
    bar_x_size = (line_x_end - line_x_start) / float(len(scale_numbers))
    for i in range(1, len(scale_numbers)):
        x_i = math.floor(tick_positions[0][0]+bar_x_size*i)
        tick_positions.append((x_i,line_y_start))
    tick_positions.append((line_x_end, line_y_start))
    # initiate remaining points, the bar height-list, continue and timer
    height_list = [0 for a in range(0, len(tick_positions))]
    remaining_points = points
    cont = False
    reset_timer = True

    while not cont:

        if reset_timer == True: # reset timer if remaining points not = 0
            timer = pygame.time.get_ticks()

        Screen.fill(white)  # draw background
        pygame.draw.line(Screen, black, (line_x_start, line_y_start), (line_x_end, line_y_end), 5) # draw scale
        drawStaticTicks(Screen, scale_numbers, tick_positions, tick_font, offset = offset, tick_mode=tick_mode,
                        custom_ticks = custom_ticks, precision = precision) # draw tick-positions
        Screen.blit(stim_img, (10,10)) # draw stimulus

        height_list, remaining_points, cont, reset_timer = drawBars(df_name, pp_info, Screen, line_y_init,
                                                                    tick_positions, points, line_x_end,
                                                                    height_list, remaining_points, continue_img,
                                                                    continue_mouseover_img, timer, min, precision,
                                                                    scale_numbers, tick_font, tick_mode,
                                                                    max_height, **kwargs)
                                                                    # handle user input

        displayPoints(Screen, line_x_init, line_y_init, remaining_points, point_font) # show remaining points

        pygame.display.update() # display the bars until cont = True
