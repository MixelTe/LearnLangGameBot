// https://cs.stanford.edu/people/eroberts/courses/soco/projects/computers-and-the-hgp/smith_waterman.html
// https://en.wikipedia.org/wiki/Smith%E2%80%93Waterman_algorithm
// http://rna.informatik.uni-freiburg.de/Teaching/index.jsp?toolName=Smith-Waterman

export function smith_waterman_algorithm(A: string, B: string, Match = 3, Dismatch = 3, Gap = 1): [number[][], [number, number][]]
{
	const n = A.length;
	const m = B.length;
	const H: number[][] = new Array(n + 1).fill(0).map(_ => new Array(m + 1).fill(0));
	let Mv = -1;
	let Mi = -1;
	let Mj = -1;
	for (let i = 1; i < n + 1; i++)
		for (let j = 1; j < m + 1; j++)
		{
			const v = H[i][j] = Math.max(
				H[i - 1][j - 1] + (A[i - 1] == B[j - 1] ? Match : -Dismatch),
				H[i - 1][j] - Gap,
				H[i][j - 1] - Gap,
				0,
			);
			if (v > Mv)
			{
				Mv = v;
				Mi = i;
				Mj = j;
			}
		}
	const p: [number, number][] = [];
	if (Mi < 0) return [H, p];
	while (H[Mi][Mj] > 0)
	{
		p.push([Mi, Mj]);
		var v1 = H[Mi - 1][Mj - 1];
		var v2 = H[Mi - 1][Mj];
		var v3 = H[Mi][Mj - 1];
		var max = Math.max(v1, v2, v3);
		if (v1 == max) { Mi--; Mj--; }
		else if (v2 == max) Mi--;
		else Mj--;
		Mv = max;
	}
	return [H, p];
}

export function string_similarity_by_smith_waterman_algorithm(A: string, B: string, Match = 3, Dismatch = 3, Gap = 1)
{
	const [_, p] = smith_waterman_algorithm(A, B, Match, Dismatch, Gap);
	let li = -1;
	let lj = -1;
	let m = 0;
	let n = 0;
	for (const [i, j] of p.reverse())
	{
		if (li != i && lj != j)
			if (A[i - 1] == B[j - 1])
				m += 1;
			else
				n += 1;
		else
			n += 0.5;
		li = i;
		lj = j;
	}

	return (m + n / 2) / Math.max(A.length, B.length);
}

export interface IStringCorItem
{
	val: string;
	cor: string;
}
export function string_correction_by_smith_waterman_algorithm(correctString: string, inputString: string, fillWord = true, Match = 3, Dismatch = 3, Gap = 1)
{
	const [_, p] = smith_waterman_algorithm(correctString, inputString, Match, Dismatch, Gap);
	const r: IStringCorItem[] = [];

	if (p.length == 0)
	{
		if (fillWord)
			for (const ch of correctString)
				r.push({ val: "", cor: ch });
		return r;
	}


	{
		const [pi, pj] = p[p.length - 1];
		let i = 0;
		if (fillWord)
			while (++i < pi && i <= pi - pj)
				r.push({ val: "", cor: correctString[i - 1] });
		i = 0;
		while (++i < pj)
			if (pi - pj + i > 0)
				r.push({ val: inputString[i - 1], cor: correctString[pi - pj + i - 1] });
			else
				r.push({ val: inputString[i - 1], cor: "" });
	}

	let lj = -1, li = -1;
	for (const [i, j] of p.slice().reverse())
	{
		if (lj != j && li != i)
			r.push({ val: inputString[j - 1], cor: correctString[i - 1] });
		else if (lj == j)
			r.push({ val: "", cor: correctString[i - 1] });
		else
			r.push({ val: inputString[j - 1], cor: "" });
		li = i;
		lj = j;
	}

	{
		const [pi, pj] = p[0];
		let i = pj;
		while (++i < inputString.length + 1)
			if (pi - pj + i < correctString.length + 1)
				r.push({ val: inputString[i - 1], cor: correctString[pi - pj + i - 1] });
			else
				r.push({ val: inputString[i - 1], cor: "" });
		if (fillWord)
			while (pi - pj + i++ < correctString.length + 1)
				r.push({ val: "", cor: correctString[pi - pj + i - 2] });
	}

	return r;
}
export function string_correction_by_smith_waterman_algorithm_to_console(correctString: string, inputString: string, Match = 3, Dismatch = 3, Gap = 1)
{
	const r = string_correction_by_smith_waterman_algorithm(correctString, inputString, true, Match, Dismatch, Gap);
	let sr = "";
	for (const v of r)
	{
		if (v.val == v.cor)
			sr += v.val + " ";
		else if (v.val == "")
			sr += "\x1b[34m[" + v.cor + "]\x1b[0m" + " ";
		else if (v.cor == "")
			sr += "\x1b[31m" + v.val + "\x1b[0m" + " ";
		else
			sr += "\x1b[31m" + v.val + ">" + v.cor + "\x1b[0m" + " ";
	}
	console.log(sr);
}

export function test()
{
	const A = "светильник";
	const B = "свитилники";
	// const A = "apple";
	// const B = "aplle";
	// const A = "дезинтеграция";
	// const B = "дезентеграция";
	// const B = "дезентграция";
	// const A = "дезинтуграци";
	// const B = "деентегрция";
	// const A = "GAGTCGC";
	// const B = "CTATGCA";
	// const A = "AAUGCCAUUGACGG";
	// const B = "CAGCCUCGCUUAG";
	// const A = "AATCG";
	// const B = "AACG";
	// const A = "GGTTGACTA";
	// const B = "TGTTACGG";
	const [R, p] = smith_waterman_algorithm(A, B);
	let line = "  #  ";
	for (const r of B)
		line += r + "  ";
	console.log(line);

	for (let i = 0; i < R.length; i++)
	{
		const r = R[i];
		line = "";
		if (i == 0)
			line = "# ";
		else
			line = A[i - 1] + " ";
		for (let j = 0; j < r.length; j++)
		{
			const v = r[j];
			let f = false;
			for (const [i1, j1] of p)
				if (i == i1 && j == j1)
				{
					f = true;
					break;
				}
			if (f)
				line += "\x1b[47m\x1b[30m";
			line += v + " ".repeat(Math.max(3 - `${v}`.length, 0));
			if (f)
				line += "\x1b[0m";
		}
		console.log(line);
	}

	console.log();
	string_correction_by_smith_waterman_algorithm_to_console(A, B);
	console.log();

	let sb = "";
	let sa = "";
	let li = -1;
	let lj = -1;
	let m = 0;
	let n = 0;
	for (const [i, j] of p.reverse())
	{
		let cs;
		let ce;
		if (li != i && lj != j)
		{
			const c = A[i - 1] != B[j - 1];
			cs = c ? "\x1b[31m" : "";
			ce = c ? "\x1b[0m" : "";
			if (c) n += 1;
			else m += 1;
		}
		else
		{
			cs = "\x1b[34m";
			ce = "\x1b[0m";
			n += 0.5;
		}
		if (li == i)
			sa += cs + "- " + ce;
		else
			sa += cs + A[i - 1] + ce + " ";
		if (lj == j)
			sb += cs + "- " + ce;
		else
			sb += cs + B[j - 1] + ce + " ";
		li = i;
		lj = j;
	}

	console.log(sb);
	console.log(sa);
	console.log("Match:", m);
	console.log("Edit:", n);
	console.log("Similarity:", (m + n / 2) / Math.max(A.length, B.length));

	console.log();
	console.log("-".repeat(20));
	console.log(string_similarity_by_smith_waterman_algorithm(A, B));
}
