.DEFAULT_GOAL := format

format:
	cargo check
	cargo fmt

test: 
	cargo test

run_iam:
	cargo run iam
