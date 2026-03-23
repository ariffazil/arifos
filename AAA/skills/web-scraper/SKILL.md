---
name: web-scraper
description: Configurable web scraping service. Extract structured data from any website. Custom projects and monthly maintenance contracts.
auto_trigger: false
---

# Web Scraper Service

汎用ウェブスクレイピングサービス。任意のサイトから構造化データを抽出。

## 収益ポテンシャル

- **単発プロジェクト**: $200-2,000
- **月額保守契約**: $50-200/月
- **月収目安**: $1,000-8,000/月

## 対応スクレイピング

### Eコマース
```
商品情報（名前、価格、画像、説明）
在庫状況
レビュー・評価
価格履歴
```

### 不動産
```
物件リスト
価格・面積・間取り
連絡先情報
エリア統計
```

### 求人
```
求人タイトル・会社名
給与・勤務地
応募要件
締切日
```

### SNS/メディア
```
投稿・コメント
フォロワー数
エンゲージメント統計
ハッシュタグ分析
```

## 使用方法

### 基本スクレイピング
```
「[URL]から商品情報をスクレイピングして」
「[サイト]の全記事タイトルを抽出」
```

### 詳細指定
```
「URL: [target_url]
 抽出項目: [name, price, image, description]
 ページ数: [max_pages]
 出力形式: [CSV/JSON/Excel]」
```

## 技術スタック（ローカル版）

### 前提条件
```bash
npm install puppeteer cheerio
```

### ブラウザベース（JavaScript必要なサイト）
```javascript
const puppeteer = require('puppeteer');

async function scrapeWithBrowser(url, extractScript) {
  const client = await createClient({ headless: true });

  await client.executeSequence([
    { type: 'navigate', url: url },
    { type: 'wait', ms: 3000 }
  ]);

  // JavaScript実行でデータ抽出
  const data = await client.page.evaluate(() => {
    return [...document.querySelectorAll('.product')].map(el => ({
      name: el.querySelector('.name')?.textContent,
      price: el.querySelector('.price')?.textContent,
      image: el.querySelector('img')?.src
    }));
  });

  await client.close();
  return data;
}
```

### HTTPベース（静的サイト）
```javascript
const cheerio = require('cheerio');

async function scrapeStatic(url) {
  const response = await fetch(url);
  const html = await response.text();
  const $ = cheerio.load(html);

  return $('.product').map((i, el) => ({
    name: $(el).find('.name').text(),
    price: $(el).find('.price').text()
  })).get();
}
```

### アンチボット対策
```javascript
// ランダム遅延
await new Promise(r => setTimeout(r, 2000 + Math.random() * 3000));

// User-Agent設定
const client = await createClient({
  userAgent: 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
});
```

## 出力フォーマット

### CSV
```csv
name,price,url,image
"Product 1","$99.99","https://...","https://..."
```

### JSON
```json
{
  "scraped_at": "2026-02-03T12:00:00Z",
  "total_items": 150,
  "data": [...]
}
```

### Excel
- フォーマット済みシート
- フィルター設定済み
- グラフ自動生成オプション

## 価格プラン

### Single Project ($200-500)
- 1サイト、1回限りの抽出
- 最大1,000件
- CSVまたはJSON出力

### Multi-Site Project ($500-1,000)
- 複数サイト対応
- データ統合・正規化
- クリーニング込み

### Enterprise ($1,000-2,000)
- 複雑なサイト対応
- API構築
- 自動スケジュール

### Monthly Maintenance ($50-200/月)
- 定期実行（日次/週次）
- データ更新通知
- スクリプト保守

## セキュリティ・倫理

### 遵守事項
- robots.txt を尊重
- 過度なリクエストを避ける
- 個人情報は収集しない
- 利用規約を確認

### 禁止事項
- ログイン必要なプライベートデータ
- 著作権保護コンテンツ
- 違法な用途
