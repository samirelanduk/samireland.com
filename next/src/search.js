const WORD_BOUNDARY = /[^a-z0-9]/;

const isWordStart = (text, index) => {
  return index === 0 || WORD_BOUNDARY.test(text[index - 1]);
}

export const matchTerm = (term, text, allowFuzzy=true) => {
  /**
   * Matches a single search term against a piece of text, returning a score
   * and the matched character indices, or null if there is no match. Exact
   * substrings score highest (with bonuses for word starts), falling back to
   * fuzzy subsequence matching for short texts like titles.
   */

  if (!term || !text) return null;
  const lowerTerm = term.toLowerCase();
  const lowerText = text.toLowerCase();

  const index = lowerText.indexOf(lowerTerm);
  if (index !== -1) {
    let score = 100 + Math.min(lowerTerm.length * 4, 40) - Math.min(index, 20);
    if (isWordStart(lowerText, index)) score += 50;
    if (index === 0) score += 25;
    const indices = [];
    for (let i = 0; i < lowerTerm.length; i++) indices.push(index + i);
    return { score, indices };
  }

  if (!allowFuzzy || lowerText.length > 120 || lowerTerm.length < 2) return null;
  const plain = subsequenceMatch(lowerTerm, lowerText, false);
  const wordStarts = subsequenceMatch(lowerTerm, lowerText, true);
  const best = [plain, wordStarts].reduce((a, b) => {
    if (!a) return b;
    if (!b) return a;
    return b.score > a.score ? b : a;
  }, null);
  if (!best || best.score < 15) return null;
  return best;
}

const subsequenceMatch = (lowerTerm, lowerText, preferWordStarts) => {
  const indices = [];
  let score = 0;
  let lastMatch = -2;
  let position = 0;
  for (const char of lowerTerm) {
    let found = -1;
    if (preferWordStarts) {
      for (let i = position; i < lowerText.length; i++) {
        if (lowerText[i] === char && isWordStart(lowerText, i)) {
          found = i;
          break;
        }
      }
    }
    if (found === -1) {
      found = lowerText.indexOf(char, position);
      if (found === -1) return null;
    }
    score += 4;
    if (found === lastMatch + 1) score += 8;
    if (isWordStart(lowerText, found)) score += 10;
    indices.push(found);
    lastMatch = found;
    position = found + 1;
  }
  const spread = indices[indices.length - 1] - indices[0] - lowerTerm.length + 1;
  score -= Math.min(spread * 2, 40);
  return { score, indices };
}

export const searchEntries = (query, entries, limit=15) => {
  /**
   * Searches index entries against a query, every term of which must match an
   * entry's title, keywords or body for it to be included. Returns the top
   * results by score, each with the entry, its score, and any title character
   * indices to highlight.
   */

  const terms = query.trim().split(/\s+/).filter(Boolean);
  if (!terms.length) return [];
  const results = [];
  for (const entry of entries) {
    let score = 0;
    let titleIndices = [];
    let allTermsMatch = true;
    for (const term of terms) {
      const title = matchTerm(term, entry.title);
      const keywords = matchTerm(term, entry.keywords);
      const body = matchTerm(term, entry.body, false);
      const best = Math.max(
        title ? title.score : 0,
        keywords ? keywords.score * 0.75 : 0,
        body ? body.score * 0.4 : 0
      );
      if (!best) {
        allTermsMatch = false;
        break;
      }
      score += best;
      if (title) titleIndices.push(...title.indices);
    }
    if (!allTermsMatch) continue;
    titleIndices = [...new Set(titleIndices)].sort((a, b) => a - b);
    results.push({ entry, score, titleIndices });
  }
  results.sort((a, b) => b.score - a.score);
  return results.slice(0, limit);
}

export const splitByIndices = (text, indices) => {
  /**
   * Splits text into segments, each marked as highlighted or not, from a
   * sorted list of highlighted character indices.
   */

  const indexSet = new Set(indices);
  const segments = [];
  for (let i = 0; i < text.length; i++) {
    const highlighted = indexSet.has(i);
    const last = segments[segments.length - 1];
    if (last && last.highlighted === highlighted) {
      last.text += text[i];
    } else {
      segments.push({ text: text[i], highlighted });
    }
  }
  return segments;
}
