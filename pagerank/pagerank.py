import os
import pprint
import random
import re
import sys

DAMPING = 0.85
SAMPLES = 10000


def main():
    if len(sys.argv) != 2:
        sys.exit("Usage: python pagerank.py corpus")
    corpus = crawl(sys.argv[1])
    ranks = sample_pagerank(corpus, DAMPING, SAMPLES)
    print(f"PageRank Results from Sampling (n = {SAMPLES})")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")
    ranks = iterate_pagerank(corpus, DAMPING)
    print(f"PageRank Results from Iteration")
    for page in sorted(ranks):
        print(f"  {page}: {ranks[page]:.4f}")


def crawl(directory):
    """
    Parse a directory of HTML pages and check for links to other pages.
    Return a dictionary where each key is a page, and values are
    a list of all other pages in the corpus that are linked to by the page.
    """
    pages = dict()

    # Extract all links from HTML files
    for filename in os.listdir(directory):
        if not filename.endswith(".html"):
            continue
        with open(os.path.join(directory, filename)) as f:
            contents = f.read()
            links = re.findall(r"<a\s+(?:[^>]*?)href=\"([^\"]*)\"", contents)
            pages[filename] = set(links) - {filename}

    # Only include links to other pages in the corpus
    for filename in pages:
        pages[filename] = set(
            link for link in pages[filename]
            if link in pages
        )

    return pages


def transition_model(corpus, page, damping_factor):
    """
    Return a probability distribution over which page to visit next,
    given a current page.

    With probability `damping_factor`, choose a link at random
    linked to by `page`. With probability `1 - damping_factor`, choose
    a link at random chosen from all pages in the corpus.
    """

    num_pages = len(corpus)
    num_links = len(corpus[page])

    p_not_damping = (1 - damping_factor) / num_pages

    tr_model = {pg: p_not_damping for pg in corpus}

    for i in range(num_links):
        linked_page = list(corpus[page])[i]
        p_damping = damping_factor / num_links
        tr_model[linked_page] += p_damping

    return tr_model


def sample_pagerank(corpus, damping_factor, n):
    """
    Return PageRank values for each page by sampling `n` pages
    according to transition model, starting with a page at random.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """
    landing_count = dict()
    landing_count = {pg: 0 for pg in corpus}

    page = random.choice(list(corpus.keys()))

    for iter in range(n):
        landing_count[page] += 1
        tr_model = transition_model(corpus, page, damping_factor)
        if max(tr_model.values()) == 0:
            is_damping = False
        else:
            is_damping = True if random.random() < damping_factor else False

        if is_damping:
            page = random.choices(list(tr_model.keys()), weights=list(tr_model.values()))[0]
        else:
            page = random.choice(list(tr_model.keys()))

    sample = {key: value / n for key, value in landing_count.items()}
    return sample


def iterate_pagerank(corpus, damping_factor):
    """
    Return PageRank values for each page by iteratively updating
    PageRank values until convergence.

    Return a dictionary where keys are page names, and values are
    their estimated PageRank value (a value between 0 and 1). All
    PageRank values should sum to 1.
    """

    # Initialize corpus of incoming links - dictionary lists incoming linking pages to each page
    pages_linking_to = dict()
    corpus_copy = corpus.copy()
    corpus_pages = {item for item in corpus}

    for page in corpus:
        if len(corpus[page]) == 0:
            corpus_copy[page] = corpus_pages

    for page in corpus_copy:
        pages_linking_to[page] = set()
        for linking_page in corpus_copy:
            if page in corpus_copy[linking_page]:
                pages_linking_to[page].add(linking_page)

    # print('Corpus copy:')
    # pprint.pprint(corpus_copy)
    # print()

    # Initialize baseline pagerank
    num_pages = len(corpus_copy)
    pagerank = {pg: 1 / num_pages for pg in corpus_copy}

    # Iterate until any correction to the pageranks is marginal (< 0.001)
    is_marginal_correction = False
    while not is_marginal_correction:
        # pprint.pprint(pagerank)
        is_marginal_correction = True
        for page in corpus_copy:
            previous_pagerank = pagerank[page]
            linking_pages = pages_linking_to[page]
            pagerank[page] = (1 - damping_factor) / num_pages
            for lp in linking_pages:
                pagerank[page] += damping_factor * pagerank[lp] / len(corpus_copy[lp])
            is_marginal_correction = is_marginal_correction and (abs(pagerank[page] - previous_pagerank) < 0.001)

    # pagerank_sum = sum(pagerank.values())
    # pagerank = {key: value / pagerank_sum for key, value in pagerank.items()}
    return pagerank


if __name__ == "__main__":
    main()
