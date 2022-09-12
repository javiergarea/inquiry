![](https://github.com/javiergarea/inquiry/blob/master/inquiry_app/static/img/inquiry.png?raw=true)

<!-- Badges -->
![](https://img.shields.io/github/license/javiergarea/inquiry)

**Inquiry** is a search engine of electronic preprints. 

For now, you can access to papers in the fields of mathematics, physics, computer science and statistics. These papers are retrieved from the [arXiv](https://arxiv.org) repository.

## Prerequisites

In order to use **Inquiry**, we assume you have met the following requirements:

* **python>=3.x**
* **elasticsearch==7.4.0**
* **gcc**
* **Poppler cpp lib**

## Installing Inquiry

To install **Inquiry**, follow these steps:

* Clone this repository:
    ```
    $ git clone https://github.com/javiergarea/inquiry.git
    ```

* Run the following command to install the project dependencies:
    ```
    $ pip3 install -r requirements.txt
    ```
    > If something goes wrong during this step, ensure you have installed ```pip```, ```gcc``` and ```popplerlib```.

## Running Inquiry

1. Run the **arXiv** spider in order to crawl the documents:
    ```
    $ scrapy crawl arxiv
    ```
    > This should generate an ```items.jsonl``` file in the root directory.

2. Start the **Elasticsearch** service:
    ```
    $ elasticsearch
    ```
    > Check that is running properly by running the command ``` curl localhost:9200 ```.

3. Index the crawled data in **Elasticsearch**:
    ```
    $ python3 elastic_manage.py -i items.jsonl
    ```

4. Run the **Inquiry** service:
    ```
    $ python3 manage.py runserver
    ```

5. Access to [localhost:8000](localhost:8000) and perform your queries.

## Documentation
**Inquiry** is an Information Retrieval project. This project has been developed as part of the MSc. in Computer Science at Universidade da Coruña. The software is accompanied by a technical document which details its development. This document is available in [web version](https://htmlpreview.github.io/?https://github.com/javiergarea/inquiry/blob/3933a8e345f83e4166455d852a9ac1ad2805c7a1/inquiry_app/templates/about.html).


## Authors
[Javier Garea](https://github.com/javiergarea) - <javier.garea@udc.es>

[Martín Sande](https://github.com/MartinSandeCosta) - <martin.sande@udc.es>


## License

This project uses the following license: [MIT](https://github.com/javiergarea/inquiry/blob/master/LICENSE).
