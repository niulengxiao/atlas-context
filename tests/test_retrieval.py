"""Retrieval contracts with invented records, independent of private source data."""
from copy import deepcopy
from datetime import datetime, timedelta, timezone
import unittest

from atlas_context.core import approve_local, make_record, query_context, resolve_evidence_local, revision


class RetrievalTests(unittest.TestCase):
    def fixture(self, texts):
        self.now = datetime.now(timezone.utc)
        self.records = [make_record(source="phone_export", source_ref="fictional-" + str(i),
                                   attribution="user_statement", title="PRIVATE_TITLE", private_text="PRIVATE_NOTE")
                        for i, _ in enumerate(texts)]
        self.grant = approve_local(self.records, [
            {"record_id": r["id"], "revision": r["revision"], "text": text}
            for r, text in zip(self.records, texts)], purpose="personal_assistance", audience="fictional_agent",
            expires_at=(self.now + timedelta(hours=1)).isoformat())

    def search(self, query="", **options):
        return query_context(self.records, self.grant, purpose="personal_assistance", audience="fictional_agent",
                             query=query, now=self.now, **options)

    def test_whole_words_punctuation_and_stable_relevance(self):
        self.fixture(["I started walking.", "I enjoy photography.", "I enjoy photography and quiet walks."])
        result = self.search("What about PHOTOGRAPHY, and quiet walks?")
        self.assertEqual([item["text"] for item in result["items"]],
                         ["I enjoy photography and quiet walks.", "I enjoy photography."])
        self.assertEqual(self.search("art")["items"], [])  # Not a substring of 'started'.
        self.assertEqual(self.search("ＰＨＯＴＯＧＲＡＰＨＹ")["items"], self.search("photography")["items"])

    def test_chinese_phrase_can_match_inside_a_question(self):
        self.fixture(["我喜欢摄影，也喜欢安静的散步。", "这些咖啡馆照片是工作任务。"])
        result = self.search("你知道我有哪些摄影兴趣吗？")
        self.assertEqual([item["text"] for item in result["items"]], ["我喜欢摄影，也喜欢安静的散步。"])
        self.assertEqual(self.search("我的雇主是谁？")["items"], [])

    def test_empty_overview_is_bounded_and_nonempty_noise_is_not_an_overview(self):
        self.fixture(["Fictional record " + str(i) for i in range(15)])
        result = self.search()
        self.assertEqual(len(result["items"]), 10)
        self.assertEqual(result["retrieval"]["mode"], "overview")
        self.assertTrue(result["retrieval"]["has_more"])
        for query in ("???", "what is the"):
            self.assertEqual(self.search(query)["items"], [])
        self.assertEqual(len(self.search(max_results=50)["items"]), 15)

    def test_character_budget_preserves_exact_wording(self):
        texts = ["a" * 1800, "b" * 1800, "c" * 1800]
        self.fixture(texts)
        result = self.search(max_chars=2500)
        self.assertEqual([item["text"] for item in result["items"]], texts[:1])
        self.assertEqual(result["retrieval"]["returned_chars"], 1800)
        self.assertTrue(result["retrieval"]["has_more"])
        self.assertEqual(len(self.search(max_chars=6000)["items"]), 3)

    def test_private_and_unapproved_records_never_affect_results_or_has_more(self):
        self.fixture(["I enjoy photography."])
        before = self.search("photography", max_results=1)
        extra = deepcopy(self.records[0])
        extra["id"] = "fictional-unapproved"
        extra["private_text"] = "photography photography"
        extra["revision"] = revision(extra)
        self.records.append(extra)
        self.assertEqual(self.search("photography", max_results=1), before)
        self.assertEqual(self.search("PRIVATE_NOTE")["items"], [])

    def test_invalid_budget_types_and_ranges_fail_closed(self):
        self.fixture(["Fictional statement"])
        for options in ({"max_results": True}, {"max_results": 1.0}, {"max_results": 0},
                        {"max_results": 51}, {"max_chars": False}, {"max_chars": 2499},
                        {"max_chars": 20001}, {"include_inferred": "false"}):
            with self.subTest(options=options), self.assertRaises(ValueError):
                self.search(**options)

    def test_citation_outside_overview_remains_resolvable_locally_until_revoked(self):
        self.fixture(["Fictional record " + str(i) for i in range(15)])
        item = self.search("14")["items"][0]
        self.assertNotIn(item, self.search()["items"])
        resolved = resolve_evidence_local(self.records, self.grant, item["citation"],
                                         purpose="personal_assistance", audience="fictional_agent", now=self.now)
        self.assertEqual(resolved["source_ref"], "fictional-14")
        self.grant["active"] = False
        with self.assertRaises(PermissionError):
            resolve_evidence_local(self.records, self.grant, item["citation"],
                                   purpose="personal_assistance", audience="fictional_agent", now=self.now)

    def test_bigger_budget_does_not_restore_inference_or_changed_records(self):
        self.fixture(["Current preference", "Inferred preference", "Stale preference"])
        self.records[1]["attribution"] = "inferred"
        self.records[1]["revision"] = revision(self.records[1])
        self.grant["approved"][1]["revision"] = self.records[1]["revision"]
        self.records[2]["private_text"] = "Changed"
        self.records[2]["revision"] = revision(self.records[2])
        self.assertEqual([x["text"] for x in self.search(max_results=50, max_chars=20000)["items"]], ["Current preference"])
