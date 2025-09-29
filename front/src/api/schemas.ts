export type Source = {
    name: string
}

export type Category = {
    name: string
}

export type Article = {
    article_name: string
    subtitle: string
    lead_text: string
    publish_date: string
    updated_at: string
    thumbnail: string
    scrapped_at: string
    origin_url: string
    source: Source
    categories: Category[]
}