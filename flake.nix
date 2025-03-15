{
  description = "A very basic flake";

  inputs = {
    nixpkgs.url = "github:nixos/nixpkgs?ref=nixos-24.11";
    flake-utils.url = "github:numtide/flake-utils";
  };

  outputs = { self, nixpkgs, flake-utils }:
    flake-utils.lib.eachDefaultSystem (system: let
      pkgs = import nixpkgs { inherit system; };
    in {
      devShells.default = pkgs.mkShell {
        packages = with pkgs; [
          python3
          uv
        ];
      };

      apps.default = flake-utils.lib.mkApp {
        drv = pkgs.writeShellScriptBin "run-main" ''
          ${pkgs.uv}/bin/uv run main.py
        '';
      };
    });
}
