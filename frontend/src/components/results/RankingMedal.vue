<template>
  <span class="ranking-medal" :class="[`ranking-medal--${variant}`, `ranking-medal--${size}`]">
    <span class="ranking-medal__number">{{ position }}</span>
  </span>
</template>

<script setup lang="ts">
withDefaults(
  defineProps<{
    position: number;
    variant?: 'gold' | 'silver' | 'bronze' | 'muted';
    size?: 'podium' | 'list';
  }>(),
  {
    variant: 'muted',
    size: 'list'
  }
);
</script>

<style scoped lang="scss">
.ranking-medal {
  position: relative;
  display: inline-grid;
  place-items: center;
  flex: 0 0 auto;
  border-radius: 50%;
  border: 2px solid var(--ws-border);
  color: var(--ws-text);
  font-family: 'Space Grotesk', 'ManropeVariable', Manrope, sans-serif;
  font-weight: 800;
  line-height: 1;
  isolation: isolate;
  box-shadow:
    inset 0 1px 0 color-mix(in srgb, #ffffff 52%, transparent),
    inset 0 -9px 16px color-mix(in srgb, #000000 18%, transparent),
    0 9px 18px color-mix(in srgb, #000000 18%, transparent);
}

.ranking-medal::after {
  content: '';
  position: absolute;
  inset: 5px 7px auto auto;
  width: 28%;
  height: 20%;
  border-radius: 999px;
  background: color-mix(in srgb, #ffffff 56%, transparent);
  filter: blur(0.2px);
  opacity: 0.75;
}

.ranking-medal--podium {
  width: 46px;
  height: 46px;
  font-size: 1rem;
}

.ranking-medal--podium::before {
  content: '';
  position: absolute;
  top: -10px;
  left: 50%;
  z-index: -1;
  width: 24px;
  height: 18px;
  transform: translateX(-50%);
  clip-path: polygon(50% 0, 100% 100%, 52% 74%, 0 100%);
  background: linear-gradient(135deg, color-mix(in srgb, currentColor 52%, transparent), color-mix(in srgb, currentColor 18%, transparent));
  opacity: 0.55;
}

.ranking-medal--list {
  width: 30px;
  height: 30px;
  font-size: 0.82rem;
  box-shadow:
    inset 0 1px 0 color-mix(in srgb, #ffffff 28%, transparent),
    inset 0 -6px 10px color-mix(in srgb, #000000 12%, transparent);
}

.ranking-medal--gold {
  color: #3b2a05;
  border-color: #b98616;
  background:
    radial-gradient(circle at 30% 24%, #fff4b8 0 16%, transparent 17%),
    linear-gradient(145deg, #ffe07a 0%, #d8a023 47%, #f6c84f 100%);
}

.ranking-medal--silver {
  color: #222934;
  border-color: #929aa7;
  background:
    radial-gradient(circle at 30% 24%, #ffffff 0 15%, transparent 16%),
    linear-gradient(145deg, #f1f5fb 0%, #aeb7c4 49%, #d9dee7 100%);
}

.ranking-medal--bronze {
  color: #321808;
  border-color: #92521f;
  background:
    radial-gradient(circle at 30% 24%, #ffd4a0 0 15%, transparent 16%),
    linear-gradient(145deg, #d99757 0%, #a95f2a 49%, #c78042 100%);
}

.ranking-medal--muted {
  color: var(--ws-text-muted);
  border-color: color-mix(in srgb, var(--ws-text-muted) 42%, var(--ws-border));
  background:
    radial-gradient(circle at 30% 24%, color-mix(in srgb, #ffffff 28%, transparent) 0 16%, transparent 17%),
    linear-gradient(145deg, color-mix(in srgb, var(--ws-surface-muted) 88%, #ffffff 8%), color-mix(in srgb, var(--ws-surface-muted) 74%, #000000 10%));
}

.ranking-medal__number {
  position: relative;
  z-index: 1;
}
</style>
