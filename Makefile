PYTHON ?= $(shell if [ -x ./.venv/bin/python3 ]; then echo ./.venv/bin/python3; else command -v python3; fi)
TECTONIC := tectonic

.PHONY: formal test sims citations pdfs manifest osf-deposit check clean

formal:
	$(PYTHON) formal/run_all_formal_verifications.py

test:
	$(PYTHON) code/tools/run_tier1_tier2_suite.py

sims:
	$(PYTHON) code/tools/run_all_sims_local.py

citations:
	$(PYTHON) code/tools/audit_citation_integrity.py
	$(PYTHON) code/tools/check_manuscript_sync.py

pdfs:
	@for pair in \
		"collection:collection.tex" \
		"value_of_trust:value_of_trust.tex" \
		"gtt:gtt.tex" \
		"tfp:tfp.tex" \
		"whitepaper:whitepaper.tex" \
		"tdf:tdf.tex"; do \
		dir=$${pair%%:*}; tex=$${pair#*:}; \
		echo "Compiling manuscripts/$$dir/$$tex..."; \
		(cd "manuscripts/$$dir" && $(TECTONIC) "$$tex") || exit 1; \
	done

manifest:
	$(PYTHON) code/tools/build_osf_sha256_manifest.py

osf-deposit: manifest
	@mkdir -p dist
	zip -r -q dist/trust_stack_v4_5_osf_bundle.zip \
		README.md CITATION.cff LICENSE LICENSE-NC requirements.txt pyproject.toml SHA256_REPRODUCIBILITY_MANIFEST.json \
		manuscripts/ figures/ formal/ protocols/ docs/ code/ \
		-x "*.venv/*" "*/__pycache__/*" "*/.lake/*" "*.DS_Store" "*/saved_models/*" "*.npy" "*.npz" "*.db" "*.whl" "*/mparts/*" "*/parts/*" "*/target/*"
	@echo "Built dist/trust_stack_v4_5_osf_bundle.zip"

check: formal citations test manifest
	@echo "ALL FORMAL PROOFS, CITATION AUDIT, TIER 1/2 SUITES, AND SHA-256 MANIFEST VERIFIED."

clean:
	rm -rf dist/
	find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
