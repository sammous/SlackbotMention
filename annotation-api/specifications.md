# Specs Sentiment Annotation API

This is the document for the specification of the Sentiment Annotation API whose purpose is to build our own annotated dataset for sentiment analysis.

## API

There are 2 endpoints:

 * /getMention
 * /annotate
 * /information

### GET /getMention

Provide a mention to be annotated

```
{   
    "status",
    "mention_id",
    "text",
}
```

### POST /annotate

Annotate a mention with a sentiment {-1, 0, 1} or if the user know, it will output 2

*Input* :

```
{
    "status",
    "mention_id"
    "sentiment"
}
```

*Output* :

Output is either `success` or `error`.

```
{
    "status": status
}
```

### GET /information

Give information about the database

```
{
    "status",
    "totalMentions",
    "totalAnnotated",
    "annotationLeft",
    "positive",
    "negative",
    "neutral",
    "idk"
}
``` 