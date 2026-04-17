import "@typespec/http";
import "@typespec/rest";
import "@typespec/openapi3";

using TypeSpec.Http;
using TypeSpec.Rest;

// Sửa từ { } sang #{ }
@service(#{
  title: "Book Management API",
})
@server("http://localhost:5000", "Local server")
namespace Library;

model Book {
  id: int32;
  title: string;
  author: string;
  publishedYear: int32;
}

model BookInput {
  title: string;
  author: string;
  publishedYear?: int32;
}

@route("/books")
@tag("Books")
interface Books {
  @get list(): Book[];

  @post create(@body book: BookInput): {
    @statusCode statusCode: 201;
  };

  @route("/{id}")
  @get read(@path id: int32): Book;

  @route("/{id}")
  @put update(@path id: int32, @body book: BookInput): {
    @statusCode statusCode: 200;
  };

  @route("/{id}")
  @delete delete(@path id: int32): {
    @statusCode statusCode: 204;
  };
}