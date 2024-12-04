let
  # Use unstable nixpkgs
  nixpkgs = fetchTarball "https://github.com/NixOS/nixpkgs/archive/nixos-unstable.tar.gz";
  pkgs = import nixpkgs {};

  # Create a shell hook to activate venv if it exists
  activateVenv = ''
    if [ -d .venv ]; then
      source .venv/bin/activate
    fi
  '';
in
pkgs.mkShell {
  nativeBuildInputs = with pkgs; [
    sqlc
    uv
    postgresql
  ];
  
  shellHook = activateVenv;
}
