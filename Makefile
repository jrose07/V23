MODE = None
NAME = v23
all:
ifneq ($(NAME), v23)
	@(find . -type f -name "*" -print0 | xargs -0 sed -i'' -e "s/v23/$(NAME)/g")
	@(mv v23/v23.tex v23/$(NAME).tex)
	@(mv v23 $(NAME))
endif
	$(MAKE) -C $(NAME) MODE=$(MODE)
	cp $(NAME)/build/tex/$(NAME).pdf $(NAME)_rosenbaum_hikade.pdf

plots:
	$(MAKE) -C $(NAME) plot

clean:
	$(MAKE) -C $(NAME) clean

.PHONY: all clean
