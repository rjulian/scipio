.DEFAULT_GOAL := format

format:
	cargo fmt

test: 
	cargo test

run_iam:
	cargo run iam
