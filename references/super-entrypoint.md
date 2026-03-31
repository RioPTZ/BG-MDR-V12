# super entrypoint

Use this as the main door to the quote engine.

## purpose
One command should be enough to move from resolved/partially-resolved structured input to a recommended execution path and, when safe, a rendered quote image.

## flow
1. inspect routing input
2. choose workflow route
3. if route is operator-fast-path:
   - build payload
   - validate
   - render
4. otherwise:
   - return the selected route
   - let the operator/agent continue with the correct branch

## important rule
Super entrypoint is not a license to skip ambiguity handling.
If route says ask-back or image-handwriting, follow that route instead of forcing render.
