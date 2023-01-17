```
{
  $jsonSchema: {
    bsonType: 'object',
    title: 'News Object Validation',
    required: [
      'headline',
      'url',
      'date',
      'provider',
      'created_at'
    ],
    properties: {
      headline: {
        bsonType: 'string',
        maxLength: 50,
        description: '\'headline\' must be a string, 50 words or less, and is required'
      },
      url: {
        bsonType: 'string',
        description: '\'url\' must be a string and is required'
      },
      date: {
        bsonType: 'date',
        description: '\'date\' must be a date type and is required'
      },
      provider: {
        bsonType: 'string',
        description: '\'provider\' must be a string and is required'
      },
      created_at: {
        bsonType: 'date',
        description: '\'created_at\' must be a date and is required'
      },
      summary: {
        bsonType: [
          'string',
          'null'
        ],
        maxLength: 500,
        description: '\'summary\' must be a string and 500 words or less if the field exists'
      },
      source: {
        bsonType: [
          'string',
          'null'
        ],
        description: '\'source\' must be a string if the field exists'
      },
      symbol: {
        bsonType: [
          'string',
          'null'
        ],
        description: '\'symbol\' must be a string if the field exists'
      },
      related: {
        bsonType: [
          'string',
          'null'
        ],
        description: '\'related\' must be a string if the field exists'
      },
      score: {
        bsonType: [
          'double',
          'null'
        ],
        description: '\'score\' must be a double if the field exists'
      }
    }
  }
}

```