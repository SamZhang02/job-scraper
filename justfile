dev: 
	uv run -m App.main

test *args:
	uv run pytest {{args}}

clean:
	rm postings
	rm ignore_this.txt
