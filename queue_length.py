#החישוב אינו מבוצע עבור פניות ימינה חופשי
#ניתן להגדיר מספר משתנים לפונקציה
#discard_green_time כאשר חיובי, החישוב מבוצע עפ"י הנחה מקלה של הכפלת אורך התור במקדם האדום של הקיבולת
#basic_lost_capacity הכוונה לקיבולת אבודה שאינה תלויה במספר התמונות, הגדלת הערך מגדילה את ערך התור
#בשלב זה מוערך כי נכון יהיה להשתמש בערך 200, ואליו להוסיף ערך של 50 עבור כל תמונה החל מן הראשונה. כלומר אובדן קיבולת של 350 עבור 3 תכנון ב3 פאזות, בשלב זה אין התייחסות מועדפת לצמתים בינעירוניים בקיבולת מוגדלת
#poisson אחוזון אליו מבוצע החישוב. נהוד להשתמש בערך בין 0.85-0.95
#l אורך מכונית, מקובל 6 מטר
#cycle_time אורך התור נקבע עבור מחזור בודד. הקטנת זמן המחזור תגדיל את אורך התור
#החישוב לא כולל את הביטוי q2 ואת העדכון ב q1 המשמשים בhcs להעריך את העיכוב הנוסף כאשר הנפח גדול מן הקיבולת ולכן לא מתאים לחישוב צמתים בכשל



def queue_length(car_sum, current_pulp_vars,
                 discard_green_time=False,
                 basic_lost_capacity=200,
                 poisson=0.95,
                 l=7,
                 phf=0.9,
                 cycle_time=120):

    import math


    queue_list=[]
    number_of_images=0
    image_string="A"
    for i in range (6):
        if current_pulp_vars["image"+image_string]>0:
            number_of_images+=1
        image_string=chr(ord(image_string)+1)


    lost_capacity=basic_lost_capacity + 50*(number_of_images)
    sum_of_images= current_pulp_vars["imageA"]+current_pulp_vars["imageB"]+current_pulp_vars["imageC"]+current_pulp_vars["imageD"]+current_pulp_vars["imageE"]+current_pulp_vars["imageF"]
    capacity_with_red=sum_of_images+lost_capacity
    y=-1
    for x in range (28):
        y+=1
        if y>6:
            y=0
        cars= car_sum[x]
        if cars==0:
            length_needed=0
            queue_list.append(length_needed)

        else:
            #print (cars)
            m= math.ceil((cars/(3600/cycle_time))/phf)
            #print (m, "=average number of cars per cycle")

            sigmar=0
            i=0
            p=1
            r = ((m ** i) * 2.71828182846 ** (-m)) / (1)
            sigmar += r
            while 1:
                i=i+1
                r= ((m**i)*2.71828182846**(-m))/(p*i)
                sigmar+=r
                p=p*i

                if (sigmar)>poisson: break

            #print (i, "=max number of cars")
            #print (i*l,"=max length for queue")
            length_needed=(i*l)
            #print (length_needed)

            if discard_green_time==True:

                movement_images_sum=0

                if x<28: direction= "W"
                if x<21: direction= "E"
                if x<14: direction= "S"
                if x<7: direction= "N"
                if y==0: movement= "r"
                if y==1: movement= "rt"
                if y==2: movement= "t"
                if y==3: movement= "tl"
                if y==4: movement= "l"
                if y==5: movement= "rtl"
                if y==6: movement= "rl"

                #print (x)
                #print (direction)
                #print (movement)

                if "A"+ direction+movement in current_pulp_vars:
                    movement_images_sum+=current_pulp_vars["imageA"]

                if "B"+ direction+movement in current_pulp_vars:
                    movement_images_sum += current_pulp_vars["imageB"]

                if "C"+ direction+movement in current_pulp_vars:
                    movement_images_sum+=current_pulp_vars["imageC"]

                if "D"+ direction+movement in current_pulp_vars:
                    movement_images_sum+=current_pulp_vars["imageD"]

                if "E"+ direction+movement in current_pulp_vars:
                    movement_images_sum+=current_pulp_vars["imageE"]

                if "F"+ direction+movement in current_pulp_vars:
                    movement_images_sum+=current_pulp_vars["imageF"]

                red_capacity= (capacity_with_red - movement_images_sum) / capacity_with_red
                #print (capacity_with_red)
                #print (movement_images_sum)
                #print (red_capacity)

                length_needed=red_capacity*length_needed
                length_needed = math.ceil(length_needed)

            queue_list.append(length_needed)


                #print ("images_sum=", images_sum)




    print (queue_list)
    return queue_list

