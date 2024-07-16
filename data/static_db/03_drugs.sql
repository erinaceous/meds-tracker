create table medications
(
    category TEXT collate NOCASE not null,
    product  TEXT collate NOCASE,
    constraint medications_pk
        primary key (category, product)
);

create index medications_category_index
    on medications (category);

create index medications_product_index
    on medications (product);
