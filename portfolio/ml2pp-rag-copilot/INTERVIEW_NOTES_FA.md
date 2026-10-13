# نکات فارسی برای توضیح پروژه در مصاحبه

## پروژه چیست؟
این پروژه یک **RAG Copilot** برای دانش مرتبط با ML2++ و forecasting است. کاربر سؤال می‌پرسد، سیستم ابتدا اسناد مرتبط را بازیابی می‌کند و سپس پاسخ LLM را فقط بر اساس همان context تولید می‌کند.

## RAG یعنی چه؟
RAG مخفف Retrieval-Augmented Generation است. قبل از اینکه LLM جواب بدهد، اطلاعات مرتبط از اسناد بازیابی می‌شود. این کار باعث می‌شود پاسخ کمتر hallucination داشته باشد و بتوانیم source را نشان دهیم.

## Chunking چیست؟
اسناد بزرگ به بخش‌های کوچک‌تر تقسیم می‌شوند. اگر chunk خیلی کوچک باشد context از بین می‌رود؛ اگر خیلی بزرگ باشد retrieval دقیق نیست. overlap کمک می‌کند اطلاعات مرزی بین دو chunk از دست نرود.

## Embedding چیست؟
Embedding متن را به یک بردار عددی تبدیل می‌کند. متن‌هایی که از نظر معنی شبیه هستند در فضای برداری به هم نزدیک می‌شوند. در این پروژه semantic mode از Sentence Transformer استفاده می‌کند.

## Top-k retrieval چیست؟
سیستم k بخش مرتبط‌تر را برمی‌گرداند. k کم ممکن است اطلاعات لازم را از دست بدهد؛ k زیاد ممکن است noise وارد prompt کند.

## Grounding چیست؟
LLM مجبور می‌شود فقط از context بازیابی‌شده استفاده کند. در prompt صریحاً گفته شده که اگر اطلاعات کافی نیست، چیزی اختراع نکند.

## چرا FastAPI؟
چون پروژه را از یک notebook به یک سرویس واقعی تبدیل می‌کند. endpointهای `/retrieve` و `/ask` نشان می‌دهند که retrieval و generation را می‌توان از طریق REST API استفاده کرد.

## Docker چه چیزی را نشان می‌دهد؟
نشان می‌دهد برنامه قابل بسته‌بندی و deploy است و فقط یک prototype محلی نیست.

## Testing و CI چه اهمیتی دارند؟
تست‌ها chunking، retrieval و prompt grounding را بررسی می‌کنند. GitHub Actions با هر تغییر تست‌ها را اجرا می‌کند. این بخش برای نقش‌های software/AI engineering مهم است.

## جواب کوتاه پیشنهادی در مصاحبه
> I built an LLM/RAG portfolio project connected to my ML2++ research. The system ingests forecasting documents, chunks them, retrieves the most relevant context using lexical or semantic retrieval, and then sends only that grounded context to an LLM through a FastAPI service. I also added Docker, unit tests, and CI so it demonstrates not only RAG concepts but also software-engineering practices.

## اگر پرسیدند چرا این پروژه را ساختی؟
بگو هدف این بود که تجربه forecasting و MDE خودم را با skills موردنیاز نقش‌های جدید AI مثل LLM, RAG, APIs and deployment ترکیب کنم.

## اگر پرسیدند چه چیزی را بعداً اضافه می‌کنی؟
- vector database مثل pgvector یا Qdrant
- hybrid retrieval و reranking
- RAG evaluation dataset
- observability و tracing
- authentication و rate limiting
- Kubernetes deployment
